import os
import json
import subprocess
import sys
import time
import logging
import random

from dotenv import load_dotenv

from CUTE_components.models import Prefix_datapoint, Failed_To_Be_Repair_datapoint, Oracle_datapoint, Test_Unit_Status, Result_datapoint
from mytemplate.bf_repair_template import compile_failed_repair_template
from mytemplate.tf_repair_template import test_failed_repair_template
from chatgpt_api.sequential_chatgpt_api_proxy import generate_chat_completion
from CUTE_components.dataset import Prefix_Dataset, Oracle_Dataset
from CUTE_components.generate_stage1 import bm25_retrived_demos4prefix, get_prefix_prompt
from CUTE_components.generate_stage2 import bm25_retrived_demos4oracle, get_oracle_prompt
from CUTE_components.validate import find_objects_with_id, find_objects_by_pro_with_ver
from CUTE_components.repair import extract_stderr_message, extract_stdout_message
from util.utils import write_to_file
from util.strUtils import fetch_method_chatgpt_out, hascode, form_complete_statement, make_classpath
from util.use_unixcoder import prefix_diversity_retriever, oracle_diversity_retriever, read_unixcoder
from util.decorators import timer

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)

message_list = [
    {"role": "system", "content": "You are a proficient and helpful assistant in java testing with JUnit4 framework."}
]

def clear_chat_history():
    '''
    重置和chatgpt的历史聊天记录
    '''
    global message_list

    message_list = [
        {"role": "system", "content": "You are a proficient and helpful assistant in java testing with JUnit framework."}]


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


def encapsulate_into_test(testbody: str, testname: str) -> str:
    return f"public void {testname} {{\n{testbody}\n}}"


# 由于不是main函数调用，所以要手动给环境变量赋值
ID_PLACEHOLDER = "<ID>"
TM_PLACEHOLDER = "<TestMethodPlaceHolder>"

# 给路径占位符赋值
pro = "binance"
# for swap demo pool
demo_pro_dict = {
    "csv":"gson",
    "gson":"csv",
    "chart":"lang",
    "lang":"chart",
    "binance":"binance"
}
res_type = "nonstop"
shot_num = 5

# 准备数据路径
prefix_queryset_dir_path = f"txt_repo/prefix/query_set/{pro}"
# prefix_demopool_dir_path = f"txt_repo/prefix/demo_pool/{pro[:-5]}" # 去掉后面的_plus
prefix_demopool_dir_path = f"txt_repo/prefix/demo_pool/{demo_pro_dict[pro]}"
oracle_demopool_dir_path = f"txt_repo/oracle/demo_pool/{demo_pro_dict[pro]}"

testClass_place_path = f"txt_repo/validation/{pro}/testClass_place.json"
testClass_dir_path = f"txt_repo/validation/{pro}/test_class_content"
# id_to_num_file = f"txt_repo/validation/{pro[:-5]}/id_to_num.txt"
common_project_to_path = "txt_repo/validation/common/pro_with_ver_to_path.json"

testunit_compile_stderr_dir_path = f"txt_repo/validation/{pro}/output/{res_type}/testunit_compile"
testunit_execute_stdout_dir_path = f"txt_repo/validation/{pro}/output/{res_type}/testunit_execute"


overall_result_file = f"txt_repo/validation/{pro}/output/{res_type}/overall_result.txt"
passed_unit_file = f"txt_repo/validation/{pro}/output/{res_type}/passed_test_unit.txt"
check_chatgpt_file = f"txt_repo/validation/{pro}/output/{res_type}/check_chatgpt.txt"
original_chatgpt_out_file = f"txt_repo/validation/{pro}/output/{res_type}/original_chatgpt_out.txt"
chat_history_file = f"txt_repo/validation/{pro}/output/{res_type}/chat_history.txt"


def compile_mytest(proName: str, test: str, id: int, err_save_path: str) -> tuple[bool, str]:
    # 确定下去哪找Test.txt文件
    with open(testClass_place_path, "r") as f:
        testClass_info = json.load(f)
    testClass_info_json_list = [dict(item) for item in testClass_info]
    pro_with_ver, test_class_name = find_objects_with_id(
        id, testClass_info_json_list)
    test_class_shell_path = os.path.join(
        testClass_dir_path, test_class_name+".txt")
    with open(test_class_shell_path, "r") as f:
        test_class_shell = f.read()
    tmp_test_class = test_class_shell.replace(TM_PLACEHOLDER, test)
    final_test_class = tmp_test_class.replace(
        ID_PLACEHOLDER, str(id))  # 至此得到了可以用于编译的测试类
    # 将测试类保存到用于编译的位置test_class_save_path
    with open(common_project_to_path, "r") as f:
        common_info = json.load(f)
    common_info_json_list = [dict(item) for item in common_info]
    focal_class_path, test_class_path, middle_path = find_objects_by_pro_with_ver(
        proName, pro_with_ver, common_info_json_list)
    test_class_save_path = test_class_path
    os.makedirs(test_class_save_path, exist_ok=True)
    test_class_save_name = test_class_name+str(id)+".java"
    write_to_file(test_class_save_path+"/" +
                  test_class_save_name, final_test_class, "w")
    # 编译
    libpath = "C:\\Libraries\\maven-3.5.0\\lib\\*"
    binance_cp_1 = "C:\\dataset\\binance-connector-java\\target\\classes"
    binance_cp_2 = "C:\\dataset\\binance-connector-java\\target\\test-classes"
    # 直接字符串相加过于ugly
    # classpath = make_classpath(focal_class_path, middle_path,
    #                            test_class_path, libpath)
    classpath = make_classpath(libpath,binance_cp_1,binance_cp_2)
    compile_command = "javac -J-Duser.language=en -cp " + classpath + \
        test_class_save_path+"\\"+test_class_save_name + " -d "+binance_cp_2
    compile_result = subprocess.run(compile_command, shell=True,
                                    capture_output=True, text=True)
    # 在返回编译编译结果之前，先把刚才的类删了
    os.remove(test_class_save_path+"/" +
              test_class_save_name)  # 调试时留下，运行时照旧remove
    if compile_result.returncode == 0:  # 编译成功
        # 只有编译成功才有.class文件可删
        os.remove(binance_cp_2+"\\unit\\" +
                  test_class_save_name.replace(".java", ".class"))
        return True, None
    else:  # 编译失败 将stderr保存下来并返回
        stderr_filename = test_class_name+str(id)+"_stderr.txt"
        stderr_filename_save_path = os.path.join( err_save_path, stderr_filename)
        # 如果编译失败三次，那么也把三次的结果写在一起
        # 把编译失败的命令写下，方便调试
        print(f"[1]compile_command : \n{compile_command}\n")
        write_to_file(stderr_filename_save_path, compile_command+"\n\n")
        print(f"[2]compile_result.returncode : \n{compile_result.returncode}\n")
        original_err = compile_result.stderr
        err_wo_waring = "\n".join([line for line in original_err.split('\n') if not line.startswith("warning")])
        print(f"[3]compile_result.stderr : \n{err_wo_waring}\n")
        print(f"[4]compile_result.stdout : \n{compile_result.stdout}\n")
        
        write_to_file(stderr_filename_save_path, err_wo_waring+"\n\n")
        
        return False, err_wo_waring


def execute_mytest(proName: str, test: str, id: int, out_save_path: str) -> tuple[bool, str]:
    # 确定下去哪找Test.txt文件
    with open(testClass_place_path, "r") as f:
        testClass_info = json.load(f)
    testClass_info_json_list = [dict(item) for item in testClass_info]
    pro_with_ver, test_class_name = find_objects_with_id(
        id, testClass_info_json_list)
    test_class_shell_path = os.path.join(
        testClass_dir_path, test_class_name+".txt")
    with open(test_class_shell_path, "r") as f:
        test_class_shell = f.read()
    tmp_test_class = test_class_shell.replace(TM_PLACEHOLDER, test)
    final_test_class = tmp_test_class.replace(
        ID_PLACEHOLDER, str(id))  # 至此得到了可以用于编译的测试类
    # 将测试类保存到用于编译的位置test_class_save_path
    with open(common_project_to_path, "r") as f:
        common_info = json.load(f)
    common_info_json_list = [dict(item) for item in common_info]
    focal_class_path, test_class_path, middle_path = find_objects_by_pro_with_ver(
        proName, pro_with_ver, common_info_json_list)
    test_class_save_path = test_class_path
    os.makedirs(test_class_save_path, exist_ok=True)
    test_class_save_name = test_class_name+str(id)+".java"
    write_to_file(test_class_save_path+"/" +
                  test_class_save_name, final_test_class, "w")
    # 编译
    libpath = "C:\\Libraries\\maven-3.5.0\\lib\\*"
    binance_cp_1 = "C:\\dataset\\binance-connector-java\\target\\classes"
    binance_cp_2 = "C:\\dataset\\binance-connector-java\\target\\test-classes"
    classpath = make_classpath(libpath,binance_cp_1,binance_cp_2)
    # classpath = make_classpath(
    #     focal_class_path, middle_path, test_class_path, middle_path+"\\generated_by_chatgpt", libpath)  # 直接字符串相加过于ugly

    compile_command = "javac -J-Duser.language=en -cp " + classpath + \
        test_class_save_path+"\\"+test_class_save_name+ " -d "+binance_cp_2

    compile_result = subprocess.run(compile_command, shell=True,
                                    capture_output=True, text=True)
    # 到这一句以前，都和compile_mytest一样
    if compile_result.returncode != 0:
        os.remove(test_class_save_path+"/"+test_class_save_name)
        original_err = compile_result.stderr
        err_wo_waring = "\n".join([line for line in original_err.split('\n') if not line.startswith("warning")])
        return False, err_wo_waring  # 如果编译失败，说明不是第一次进入执行
    # 执行测试类
    execute_command = "java -cp " + classpath + " org.junit.runner.JUnitCore " + \
        "unit."+ test_class_name+str(id)

    test_result = subprocess.run(
        execute_command, shell=True, capture_output=True, text=True)
    if test_result.returncode == 0:  # 执行成功
        return True, None
    else:  # 执行失败 将stdout保存下来并返回
        stdout_filename = test_class_name+str(id)+"_stdout.txt"
        stdout_filename_save_path = os.path.join(
            out_save_path, stdout_filename)
        # 如果执行失败2次，那么也把2次的结果写在一起
        # 把执行失败的命令写下，方便调试
        print(f"[1]execute_command : \n{execute_command}\n")
        print(f"[2]test_result.returncode : \n{test_result.returncode}\n")
        print(f"[3]test_result.stderr : \n{test_result.stderr}\n")
        print(f"[4]test_result.stdout : \n{test_result.stdout}\n")
        write_to_file(stdout_filename_save_path, execute_command+"\n\n")
        write_to_file(stdout_filename_save_path, test_result.stdout+"\n\n")
        return False, test_result.stdout


def repair_bf(test_with_only_prefix: str, compile_out: str, query: Prefix_datapoint, chatgpt_max_num: int) -> str:
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
            write_to_file(original_chatgpt_out_file,
                          chatgpt_response+"\n\n" + '*'*150+'\n')
            break
    if not has_code_flg:
        logger.warning(f"repair_bf -- has_code_flg : {has_code_flg}")
        return ""
    # 输出奇奇怪怪，获取有用的代码块
    code_block = fetch_method_chatgpt_out(chatgpt_response)
    return code_block


def repair_tf_test_unit(test_unit: str, execute_out: str, query: Prefix_datapoint, chatgpt_max_num: int) -> str:
    # 从execute_out中提取出有效部分
    useful_execute_out = extract_stdout_message(execute_out)
    assert useful_execute_out is not None
    datapoint = Failed_To_Be_Repair_datapoint(
        query.classname, query.focalname_paralist, useful_execute_out, test_unit)
    # 构建prompt
    tf_repair_prompt = test_failed_repair_template(datapoint)

    # 从下面开始和repair_bf一样
    has_code_flg = False
    for i in range(1, chatgpt_max_num, 1):  # retry外包状态码的问题，这里解决空值和不含代码的问题
        write_to_file(check_chatgpt_file, f"第{i}次调用chatgpt 用于修复执行错误\n")
        chatgpt_response = call_chatgpt(tf_repair_prompt)
        # time.sleep(6)
        if hascode(chatgpt_response):  # 如果调用返回中包含代码块(而不仅仅是抱歉)，就跳出循环
            has_code_flg = True
            write_to_file(original_chatgpt_out_file,
                          chatgpt_response+"\n\n" + '*'*150+'\n')
            break
    if not has_code_flg:
        logger.warning(f"repair_tf -- has_code_flg : {has_code_flg}")
        return ""
    # 输出奇奇怪怪，获取有用的代码块
    code_block = fetch_method_chatgpt_out(chatgpt_response)
    return code_block

@timer
def main():

    # 设置一个logger，取代导出散落的print
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    load_dotenv()
    # 读取环境变量
    querynum_dict_str = os.getenv("QUERYNUM_DICT")
    querynum_dict = json.loads(querynum_dict_str)
    # testunit_compile_num = int(os.getenv("TESTUNIT_COMPILE_NUM"))
    # testunit_execute_num = int(os.getenv("TESTUNIT_EXECUTE_NUM"))

    chatgpt_max_num = int(os.getenv("CHATGPT_MAX_NUM"))
    sample_order = os.getenv("SAMPLE_ORDER")
    ORACLE_PLACEHOLDER = os.getenv("ORACLE_PLACEHOLDER")
    selector = os.getenv("SELECTOR")
    logger.info(f"selector : {selector}")

    # sample_idx_lst_dict_str = os.getenv("NEW_SAMPLE_IDX_LST_DICT")
    # sample_idx_lst_dict = json.loads(sample_idx_lst_dict_str)
    # picked_list = sample_idx_lst_dict[pro]

    prefix_queryset = Prefix_Dataset(
        prefix_queryset_dir_path,
        "constr_sign.txt",
        "fake_test_input.txt",
        "classname.txt",
        "focalname_paralist.txt",
        "test_name.txt"
    )
    prefix_queryset_list = prefix_queryset.parse()
    assert len(prefix_queryset_list) == querynum_dict[pro]

    prefix_demopool = Prefix_Dataset(
        prefix_demopool_dir_path,
        "constr_sign.txt",
        "test_input.txt",
        "classname.txt",
        "focalname_paralist.txt",
        "test_name.txt"
    )

    if selector == "unixcoder":
        prefix_unixcoder_tensor_file = os.path.join(
            prefix_queryset_dir_path, "unixcoder_tensor.txt")  # 只有用了unixcoder才要这句
        
        prefix_unixcoder_tensor_list = read_unixcoder(
            prefix_unixcoder_tensor_file)  # 只有用了unixcoder才要这句

    # m_n_tuple_str = os.getenv("N_M")
    # parsed_list = eval(m_n_tuple_str)  # 解析字符串为Python对象
    # m_n_tuple_list = [tuple(item) for item in parsed_list]
    # for m_n_tuple in m_n_tuple_list:
    testunit_compile_num, testunit_execute_num = 4,3 # m_n_tuple

    
    result_datapoint_list = []
    # 进入循环啦
    start_idx = 1  # 1
    end_idx = 100  # len(prefix_queryset_list)
    aborted_num = 0
    
    bf_num, tf_num, passed_num = 0, 0, 0

    for id in range(start_idx, end_idx+1, 1):
        try:
            # for id in [8]:
            logger.info(f"💫来到第{id}个输入，还剩{len(prefix_queryset_list)-id}个💫")

            result_datapoint = Result_datapoint(
                id, 0, 0, Test_Unit_Status.NONE_STATUS)

            tmp_query = prefix_queryset_list[id-1]
            
            now_prefix_demopool_list = prefix_demopool.parse()
            # 不同检索器走不同分支
            if selector == "unixcoder":
                
                tmp_query_tensor = prefix_unixcoder_tensor_list[id-1]
                prefix_candidate_demos,demo_sim_list = prefix_diversity_retriever(
                    tmp_query_tensor, now_prefix_demopool_list, shot_num)
                
                if sample_order == "ascending":
                    sorted_prefix_candidate_demos = [
                        tu[1] for tu in sorted(
                            enumerate(prefix_candidate_demos),key=lambda tu:demo_sim_list[tu[0]],reverse=False
                        )
                    ]
                elif sample_order == "descending":
                    sorted_prefix_candidate_demos = [
                        tu[1] for tu in sorted(
                            enumerate(prefix_candidate_demos),key=lambda tu:demo_sim_list[tu[0]],reverse=True
                        )
                    ]
            elif selector == "real_random":
                prefix_candidate_demos = random.sample(
                    now_prefix_demopool_list, shot_num)
            
                    
            # if selector == "bm25":
            #     now_prefix_demopool_list = prefix_demopool.parse(
            #         query_id=tmp_query.classname+tmp_query.focalname_paralist)
            #     prefix_candidate_demos = bm25_retrived_demos4prefix(
            #         tmp_query, now_prefix_demopool_list, sample_order, shot_num)

            if sample_order == "ascending" or sample_order == "descending":
                prefix_gen_prompt = get_prefix_prompt(
                    sorted_prefix_candidate_demos, tmp_query)
            else:
                prefix_gen_prompt = get_prefix_prompt(
                    prefix_candidate_demos, tmp_query)

            logger.info('-'*100)
            # 生成prefix
            # write_to_file(chat_history_file, ">>1<< \n")
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
                        f"生成的prefix为：{return_prefix}  \n"+'-'*100 + '\n')
            
            # 将prefix封装进test
            test_with_only_prefix = encapsulate_into_test(
                return_prefix, tmp_query.testname)
            write_to_file(check_chatgpt_file,
                        f"封装后的test_with_only_prefix为：\n{test_with_only_prefix}  \n" + '-'*100 + '\n')

            test_with_only_prefix = test_with_only_prefix.strip()
            # 至此拿到了 public void testGetTriggers() { final Argument arg = buildTargetsArgument(); }
            # oracle生成
            if test_with_only_prefix != "":
                query_test_method = test_with_only_prefix[:-1] + \
                    ORACLE_PLACEHOLDER + "\n" + test_with_only_prefix[-1]
            else:
                query_test_method = "public void " + \
                    tmp_query.testname + "{ " + ORACLE_PLACEHOLDER + "}"
            query_datapoint = Oracle_datapoint(
                query_test_method, tmp_query.focalname_paralist, tmp_query.testname, "")

            oracle_demopool = Oracle_Dataset(
                oracle_demopool_dir_path,
                "test_method.txt",
                "focalname_paralist.txt",
                "test_name.txt",
                "oracle.txt"
            )
            oracle_demopool_list = oracle_demopool.demopool_parse()

            # 这里决定用哪种检索器,too
            if selector == "unixcoder":
                oralce_candidate_demos, demo_sim_list = oracle_diversity_retriever(
                    query_datapoint, oracle_demopool_list, shot_num)
                if sample_order == "ascending":
                    sorted_oralce_candidate_demos = [
                        tu[1] for tu in sorted(
                            enumerate(oralce_candidate_demos), key=lambda tu:demo_sim_list[tu[0]], reverse=False
                        )
                    ]
                elif sample_order == "descending":
                    sorted_oralce_candidate_demos = [
                        tu[1] for tu in sorted(
                            enumerate(oralce_candidate_demos), key=lambda tu:demo_sim_list[tu[0]], reverse=True
                        )
                    ]
            elif selector == "real_random":
                oralce_candidate_demos = random.sample(
                    oracle_demopool_list, shot_num)

            # if selector == "bm25":
            #     oralce_candidate_demos = bm25_retrived_demos4oracle(
            #         query_datapoint, oracle_demopool_list, sample_order, shot_num)
            if sample_order == "ascending" or sample_order == "descending":
                oracle_gen_prompt = get_oracle_prompt(
                    sorted_oralce_candidate_demos, query_datapoint)
            else:
                oracle_gen_prompt = get_oracle_prompt(
                    oralce_candidate_demos, query_datapoint)

            return_oracle = ""
            # write_to_file(chat_history_file, ">>3<< \n")
            clear_chat_history()  # 生成oracle 第三个清空聊天记录节点
            for i in range(1, chatgpt_max_num, 1):  # retry外包状态码的问题，这里解决空值和不含代码的问题
                write_to_file(check_chatgpt_file,
                            f"第{i}次调用chatgpt 用于生成oralce\n")
                return_oracle = call_chatgpt(oracle_gen_prompt)
                # time.sleep(6)
                if return_oracle != "":  # 如果调用返回正常，就跳出循环
                    break
            return_oracle = form_complete_statement(return_oracle)
            write_to_file(check_chatgpt_file,
                        f"生成的oralce为：\n{return_oracle}  \n"+'-'*100 + '\n')
            test_unit = query_test_method.replace(
                ORACLE_PLACEHOLDER, return_oracle)

            # print("至此一个完整的测试用例生成了:\n", test_unit)
            # print('-'*100)

            # 对test_unit进行编译，如果testunit_compile_num次都不通过就中断这一次的生成
            # write_to_file(chat_history_file, ">>4<< \n")
            clear_chat_history()  # 修复test_unit的编译错误 第4个清空聊天记录节点
            compile_success = False
            for turn in range(1, testunit_compile_num+1, 1):
                compile_res, compile_out = compile_mytest(
                    pro, test_unit, id, testunit_compile_stderr_dir_path)
                result_datapoint.test_unit_compile_time += 1
                if compile_res:
                    logger.info(f"test unit 在第{turn}轮编译成功")
                    compile_success = True
                    break
                else:
                    if turn != testunit_compile_num:  # 至多修复testunit_compile_num-1次
                        logger.info(f"test unit 在第{turn}轮编译失败，进行修复")
                        test_unit = repair_bf(
                            test_unit, compile_out, tmp_query, chatgpt_max_num)  # 这里不对，第三个参数是Prefix_datapoint，不是Oracle_datapoint, 应想办法解决，或者干脆传入Prefix_datapoint?
                        write_to_file(
                            check_chatgpt_file, f"完成第{turn}次修复，修复后的test_unit为：\n{test_unit}\n" + '-'*100 + '\n')
            if not compile_success:
                logger.info(f"test unit {testunit_compile_num}次编译均失败，放弃这一次的生成")
                result_datapoint.test_unit_status = Test_Unit_Status.NOT_COMPILE_SUCCESS
                result_datapoint_list.append(result_datapoint)
                continue

            # 编译通过后，执行test_unit，如果testunit_execute_num次都不通过，也就作为最后结果
            # write_to_file(chat_history_file, ">>5<< \n")
            clear_chat_history()  # 修复test_unit的执行错误 第5个(also the last one)清空聊天记录节点
            execute_success = False
            for cycle in range(1, testunit_execute_num+1, 1):
                execute_res, execute_out = execute_mytest(
                    pro, test_unit, id, testunit_execute_stdout_dir_path)
                result_datapoint.test_unit_execute_time += 1
                if execute_res:
                    logger.info(f"test unit 在第{cycle}轮执行成功")
                    execute_success = True
                    break
                else:
                    if cycle != testunit_execute_num:  # 至多修复testunit_execute_num-1次
                        logger.info(f"test unit 在第{cycle}轮执行失败，进行修复")
                        test_unit = repair_tf_test_unit(
                            test_unit, execute_out, tmp_query, chatgpt_max_num)
                        write_to_file(
                            check_chatgpt_file, f"完成第{cycle}次修复，修复后的test_unit为：\n{test_unit}\n"+'-'*100 + '\n')
            if not execute_success:
                logger.info(f"test unit {testunit_execute_num}次执行均失败，放弃这一次的生成")
                logger.info(f"最终没有生成可以执行通过的用例"+'\n'+'-'*100+'\n')
                result_datapoint.test_unit_status = Test_Unit_Status.COMPILE_SUCCESS_BUT_NOT_EXECUTE
            else:
                print(f"测试通过~~~"+'\n'+'-'*100+'\n')
                test_unit = test_unit.replace("\n", " ")
                result_datapoint.passed_test_unit = test_unit
                result_datapoint.test_unit_status = Test_Unit_Status.EXECUTE_SUCCESS

            write_to_file(check_chatgpt_file, "#"*100+"\n")
            write_to_file(overall_result_file, result_datapoint.toString())

            status = result_datapoint.test_unit_status
            # times = int(id_to_num_list[now_id-1])
            if status == Test_Unit_Status.NOT_COMPILE_SUCCESS:
                bf_num += 1 # times
                write_to_file(passed_unit_file, str(result_datapoint.id)+", \n")
            elif status == Test_Unit_Status.COMPILE_SUCCESS_BUT_NOT_EXECUTE:
                tf_num += 1 # times
                write_to_file(passed_unit_file, str(result_datapoint.id)+", \n")
            elif status == Test_Unit_Status.EXECUTE_SUCCESS:
                passed_num += 1  # times
                write_to_file(passed_unit_file,
                            str(result_datapoint.id)+", "+result_datapoint.passed_test_unit+"\n")
            else:
                raise Exception("出现了不应该出现的结果状态")
        except Exception as e:
            logger.info(f"main got an exception: {e}")
            logger.info(f"继续执行第{id+1}个输入")
            aborted_num += 1
            continue
    ''' 对完整项目的生成结果进行统计和保存,结果可能落入这么几个区间
    3个大类区间
    1. 编译失败
    2. 编译成功，执行失败
    3. 编译成功，执行成功
    其中每个大类区间又细分为
    1. 编译失败
    1.1 test_with_only_prefix编译失败，没有进行oracle生成
    1.2 test_with_only_prefix编译成功，进行了oracle生成，但是test_unit编译失败
    2. 编译成功，执行失败
    test_with_only_prefix和test_unit各编译失败几次
    3. 编译成功，执行成功
    test_with_only_prefix和test_unit各编译失败几次，test_unit执行失败几次

    '''
    # for result_datapoint in result_datapoint_list:
    #     write_to_file(overall_result_file, result_datapoint.toString())

    # 现在是需要填论文表格的结果
    # with open(id_to_num_file, "r") as f:
    #     id_to_num_list = f.readlines()
    # bf_num, tf_num, passed_num = 0, 0, 0
    # for result_datapoint in result_datapoint_list:
    #     now_id = result_datapoint.id
    #     status = result_datapoint.test_unit_status
    #     # times = int(id_to_num_list[now_id-1])
    #     if status == Test_Unit_Status.NOT_COMPILE_SUCCESS:
    #         bf_num += 1 # times
    #         write_to_file(passed_unit_file, str(result_datapoint.id)+", \n")
    #     elif status == Test_Unit_Status.COMPILE_SUCCESS_BUT_NOT_EXECUTE:
    #         tf_num += 1 # times
    #         write_to_file(passed_unit_file, str(result_datapoint.id)+", \n")
    #     elif status == Test_Unit_Status.EXECUTE_SUCCESS:
    #         passed_num += 1  # times
    #         write_to_file(passed_unit_file,
    #                     str(result_datapoint.id)+", "+result_datapoint.passed_test_unit+"\n")
    #     else:
    #         raise Exception("出现了不应该出现的结果状态")

    # 最后把整体的情况写入到overall_output中
    # 打印整个项目的运行结果
    total_num = bf_num + tf_num + passed_num

    # 输出每种类型的绝对数量和所占比例
    percentage = (aborted_num / total_num) * 100
    write_to_file(overall_result_file,
                  f"\n\naborted : {aborted_num} ({percentage:.2f}%) \n")
    percentage = (bf_num / total_num) * 100
    write_to_file(overall_result_file,
                f"build failed : {bf_num} ({percentage:.2f}%) \n")
    percentage = (tf_num / total_num) * 100
    write_to_file(overall_result_file,
                f"test failed : {tf_num} ({percentage:.2f}%) \n")
    percentage = (passed_num / total_num) * 100
    write_to_file(overall_result_file,
                f"passed : {passed_num} ({percentage:.2f}%) \n")
    
    print(f"刚刚结束的是:{pro} from {start_idx} to {end_idx}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"总耗时: {minutes} min {seconds} sec")
 