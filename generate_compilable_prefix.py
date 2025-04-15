"""
File: 
    generate_compilable_prefix.py
Description: 
    截取自CUTE_pileline.py
    生成单个项目的可编译的test cases with only prefixes(evosuite/attempt-x/prefixes.txt)
    用于变异，之后再生成test oralces，再去和evosuite比较覆盖率
    !待实现：确定编译无误之后再保存到文件中
Author: 
    wxy
Create Date: 
    2023.12.29
Last Update Date:
    2024.1.2
Usage: 
    设置本文件的global value : pname和attempt后直接在图形界面运行
    设置.env的PROJECT
Input Parameters:  
    (1)项目名称pname
    (2)第多少次跑这个项目attempt-X
Output Files: 
    (1)中间日志文件check_chatgpt_file
    (2)结果文件test_with_only_prefix_file
"""

import os
import json
import logging
import subprocess

from chatgpt_api.sequential_chatgpt_api_proxy import generate_chat_completion
from mytemplate.bf_repair_template import compile_failed_repair_template
from CUTE_components.models import Prefix_datapoint, Failed_To_Be_Repair_datapoint
from CUTE_components.dataset import Prefix_Dataset
from CUTE_components.generate_stage1 import get_prefix_prompt
from CUTE_components.repair import extract_stderr_message
from CUTE_components.validate import find_objects_with_id, find_objects_by_pro_with_ver
from util.utils import write_to_file
from util.strUtils import fetch_method_chatgpt_out, hascode, form_complete_statement, make_classpath
from util.use_unixcoder import read_unixcoder, prefix_diversity_retriever

win10_path_prefix = "C:/codes/CodeX/vlis7_backup/CodeX_back_to_chatgpt/"

pname = "gson_plus"
attempt = "attempt-1"

prefix_queryset_dir_path = f"txt_repo/prefix/query_set/{pname}"
prefix_demopool_dir_path = f"txt_repo/prefix/demo_pool/{pname[:-5]}" # 去掉后面的_plus
check_chatgpt_file = f"txt_repo/validation/{pname[:-5]}/output/mujava/{attempt}/mujava_prefix_log.txt"
test_with_only_prefix_file = f"txt_repo/validation/{pname[:-5]}/output/mujava/{attempt}/prefixes.txt"
testClass_place_path = f"txt_repo/validation/{pname[:-5]}/evo_testClass_place.json"
testClass_dir_path = f"txt_repo/validation/{pname[:-5]}/test_class_plus_content"
evo_common_project_to_path = "txt_repo/validation/common/pro_with_ver_to_path.json"
testunit_compile_stderr_dir_path = f"txt_repo/validation/{pname[:-5]}/output/mujava/{attempt}/testunit_compile"

ID_PLACEHOLDER = "<ID>"
TM_PLACEHOLDER = "<TestMethodPlaceHolder>"
DEFAULT_CHATGPT_ROLE_DICT = {"role": "system", "content": "You are a proficient and helpful assistant in java testing with JUnit4 framework."}

message_list = [ DEFAULT_CHATGPT_ROLE_DICT ]

logger = logging.getLogger(__name__)

def clear_chat_history():
    '''
    重置和chatgpt的历史聊天记录
    '''
    global message_list

    message_list = [ DEFAULT_CHATGPT_ROLE_DICT ]

def call_chatgpt(prompt_str):
    # 提问环节
    one_question = {"role": "user", "content": prompt_str}
    message_list.append(one_question)
    answer = generate_chat_completion(message_list)
    # 善后环节
    one_talk = {"role": "assistant", "content": answer}
    message_list.append(one_talk)
    # 返回结果
    return answer

def encapsulate_into_test(testbody: str, testname: str, attempt_id : int, query_id : int) -> str:
    testname_af_number = testname[:-2]+"_"+str(attempt_id)+"_"+str(query_id)+"()"
    test_with_only_prefix = f"public void {testname_af_number}"+"{ "+f"{testbody}" +" }"
    test_with_only_prefix_in_one_line = test_with_only_prefix.replace("\n", " ")
    return test_with_only_prefix_in_one_line

def repair_bf(test_with_only_prefix: str, compile_out: str, query: Prefix_datapoint, chatgpt_max_num: int) -> str:
    '''
    输入：uncompilable test_with_only_prefix
    输出：compilable test_with_only_prefix
    '''
    # 从compile_out中提取出有效部分
    useful_compile_out = extract_stderr_message(compile_out)
    assert useful_compile_out is not None
    datapoint = Failed_To_Be_Repair_datapoint(
        query.classname, query.focalname_paralist, useful_compile_out, test_with_only_prefix)
    # 构建prompt
    bf_repair_prompt = compile_failed_repair_template(datapoint)

    has_code_flg = False
    for i in range(1, chatgpt_max_num, 1):  # retry外包状态码的问题，这里解决空值和不含代码的问题
        write_to_file(check_chatgpt_file, f"第{i}次调用chatgpt (用于修复编译错误)\n")
        chatgpt_response = call_chatgpt(bf_repair_prompt)
        # time.sleep(6)
        if hascode(chatgpt_response):  # 如果调用返回中包含代码块(而不仅仅是抱歉)，就跳出循环
            has_code_flg = True
            break
    if not has_code_flg:
        logger.warning(f"repair_bf -- has_code_flg : {has_code_flg}")
        return ""
    # 输出奇奇怪怪，获取有用的代码块
    code_block = fetch_method_chatgpt_out(chatgpt_response)
    return code_block

def compile_mytest(proName: str, test: str, id: int, err_save_path: str) -> tuple[bool, str]:
    '''
    输出：是否编译成功+编译标准错误
    '''
    # 确定下去哪找Test.txt文件
    with open(testClass_place_path, "r") as f:
        testClass_info = json.load(f)
    testClass_info_json_list = [dict(item) for item in testClass_info]
    pro_with_ver, test_class_name = find_objects_with_id( id, testClass_info_json_list)
    test_class_shell_path = os.path.join( testClass_dir_path, test_class_name+".txt")
    with open(test_class_shell_path, "r") as f:
        test_class_shell = f.read()
    tmp_test_class = test_class_shell.replace(TM_PLACEHOLDER, test)
    final_test_class = tmp_test_class.replace(
        ID_PLACEHOLDER, str(id))  # 至此得到了可以用于编译的测试类
    # 将测试类保存到用于编译的位置test_class_save_path
    with open(evo_common_project_to_path, "r") as f:
        common_info = json.load(f)
    common_info_json_list = [dict(item) for item in common_info]
    logger.info(f"✨Ready to unpack")
    focal_class_path, test_class_path, middle_path = find_objects_by_pro_with_ver(
        proName, pro_with_ver, common_info_json_list)
    logger.info(f"✨Unpack finished")
    test_class_save_path = os.path.join(
        test_class_path, middle_path, "generated_by_chatgpt")
    os.makedirs(test_class_save_path, exist_ok=True)
    test_class_save_name = test_class_name+str(id)+".java"
    write_to_file(test_class_save_path+"/" +
                  test_class_save_name, final_test_class, "w")
    # 编译
    libpath = "C:\\Libraries\\maven-3.5.0\\lib\\*"
    # 直接字符串相加过于ugly
    classpath = make_classpath(focal_class_path, middle_path,
                               test_class_path, middle_path+"\\generated_by_chatgpt", libpath)
    compile_command = "javac -J-Duser.language=en -cp " + classpath + \
        test_class_save_path+"\\"+test_class_save_name
    logger.info(f"✨Ready to compile")
    compile_result = subprocess.run(compile_command, shell=True,
                                    capture_output=True, text=True)
    logger.info(f"✨Compile finished")
    # 在返回编译编译结果之前，先把刚才的类删了
    os.remove(test_class_save_path+"/" +
              test_class_save_name)  # 调试时留下，运行时照旧remove
    if compile_result.returncode == 0:  # 编译成功
        logger.info(f"✨Compile successfully")
        # 只有编译成功才有.class文件可删
        os.remove(test_class_save_path+"/" +
                  test_class_save_name.replace(".java", ".class"))
        return True, None
    else:  # 编译失败 将stderr保存下来并返回
        logger.info(f"✨Compile failed")
        stderr_filename = test_class_name+str(id)+"_stderr.txt"
        stderr_filename_save_path = os.path.join(err_save_path, stderr_filename)
        # 如果编译失败三次，那么也把三次的结果写在一起
        # 把编译失败的命令写下，方便调试
        write_to_file(stderr_filename_save_path, f"id = {id}\n")
        write_to_file(stderr_filename_save_path, compile_command+"\n\n")
        print(f"[1]compile_command : \n{compile_command}\n")
        print(f"[2]compile_result.returncode : \n{compile_result.returncode}\n")
        print(f"[3]compile_result.stderr : \n{compile_result.stderr}\n")
        print(f"[4]compile_result.stdout : \n{compile_result.stdout}\n")
        
        write_to_file(stderr_filename_save_path, compile_result.stderr+"\n\n")
        
        return False, compile_result.stderr

def main():

    # 设置一个logger，取代导出散落的print
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    querynum_dict = {"gson_plus": 85, "cli_plus": 75, "csv_plus": 69, "chart_plus": 764, "lang_plus": 368}
    chatgpt_max_num = 3
    testunit_compile_num = 4

    prefix_queryset = Prefix_Dataset(
        prefix_queryset_dir_path,
        "constr_sign.txt",
        "fake_test_input.txt",
        "classname.txt",
        "focalname_paralist.txt",
        "test_name.txt"
    )
    prefix_queryset_list = prefix_queryset.parse()
    assert len(prefix_queryset_list) == querynum_dict[pname]

    prefix_demopool = Prefix_Dataset(
        prefix_demopool_dir_path,
        "constr_sign.txt",
        "test_input.txt",
        "classname.txt",
        "focalname_paralist.txt",
        "test_name.txt"
    )

    prefix_unixcoder_tensor_file = os.path.join(
            prefix_queryset_dir_path[:-5], "unixcoder_tensor.txt")  
    prefix_unixcoder_tensor_list = read_unixcoder(
        prefix_unixcoder_tensor_file)  

    start_idx = 11  # 1
    end_idx = len(prefix_queryset_list)  # len(prefix_queryset_list)
    for id in range(start_idx, end_idx+1, 1):
        try:
            logger.info(f"💫来到第{id}个输入，还剩{len(prefix_queryset_list)-id}个💫")
            tmp_query = prefix_queryset_list[id-1]
            now_prefix_demopool_list = prefix_demopool.parse()
            tmp_query_tensor = prefix_unixcoder_tensor_list[id-1]
            prefix_candidate_demos,_ = prefix_diversity_retriever(
                tmp_query_tensor, now_prefix_demopool_list, 5)
            prefix_gen_prompt = get_prefix_prompt(
                    prefix_candidate_demos, tmp_query)
            logger.info('-'*100)
            clear_chat_history()  # 当前query的首次调用，自然清空上一次的聊天记录
            return_prefix = ""
            for i in range(1, chatgpt_max_num, 1):  # retry外包状态码的问题，这里解决空值和不含代码的问题
                write_to_file(check_chatgpt_file,
                            f"第{i}次调用chatgpt 用于生成prefix\n")
                return_prefix = call_chatgpt(prefix_gen_prompt)
                # time.sleep(6)
                if return_prefix != "":  # 如果调用返回正常，就跳出循环
                    break
            return_prefix = form_complete_statement(return_prefix)
            write_to_file(check_chatgpt_file,
                        f"最初生成的prefix为：{return_prefix}  \n"+'-'*100 + '\n')

            # 将prefix封装进test
            test_with_only_prefix = encapsulate_into_test(
                return_prefix, tmp_query.testname, int(attempt[-1]), id)
            
            # 确保当前的test_with_only_prefix是可编译的后,才保存下来
            clear_chat_history()
            compile_success = False
            for turn in range(1, testunit_compile_num+1, 1):
                compile_res, compile_out = compile_mytest(
                    pname[:-5], test_with_only_prefix, id, testunit_compile_stderr_dir_path)
                if compile_res:
                    logger.info(f"test unit 在第{turn}轮编译成功")
                    compile_success = True
                    break
                else:
                    if turn != testunit_compile_num:  # 至多修复testunit_compile_num-1次
                        logger.info(f"test unit 在第{turn}轮编译失败，进行修复")
                        test_with_only_prefix = repair_bf(
                            test_with_only_prefix, compile_out, tmp_query, chatgpt_max_num)
            if compile_success:
                test_with_only_prefix = test_with_only_prefix.replace("\n", " ")
                write_to_file(test_with_only_prefix_file,
                            f"{id} , {test_with_only_prefix}\n")


        except Exception as e:
            logger.info(f"main got an exception: {e}")
            logger.info(f"继续执行第{id+1}个输入")
            continue


if __name__ == "__main__":
    main()
