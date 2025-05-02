# for RQ2 (non-stop v.s. casceded)
import os
import sys
import time
import json
import logging

from dotenv import load_dotenv
from typing import List

from CUTE_components.models import Testcase_datapoint, Test_Unit_Status, Result_datapoint
from CUTE_components.dataset import Testcase_Dataset
from prompt.prompt_testbody_query import TestcasePrompt
from CUTE_pipeline import clear_chat_history, call_chatgpt, compile_mytest, execute_mytest, repair_bf, repair_tf_test_unit
from util.strUtils import form_complete_statement, fetch_method_chatgpt_out
from util.use_unixcoder import testcase_diversity_retriever
from util.utils import write_to_file


ID_PLACEHOLDER = "<ID>"
TM_PLACEHOLDER = "<TestMethodPlaceHolder>"

message_list = [
    {"role": "system", "content": "You are a proficient and helpful assistant in java testing with JUnit4 and Mockito frameworks."}
]


def get_testbody_prompt(demos: List[Testcase_datapoint], query: Testcase_datapoint) -> str:
    '''
    构造few-shot learning的prompt
    query和demo的差别在于query的test_body为空字符串
    '''
    prompt = TestcasePrompt(demos, query)
    return prompt.construct_prompt()


def main():
    # 获取命令行参数
    # args = sys.argv
    # if len(args) != 3:
    #     print("Usage: python -m  non_stop_pipeline <project_name> <start_idx>")
    #     exit(1)
    # else:
    #     pro = args[1]
    #     start_idx = int(args[2])

    pro = 'binance'
    start_idx = 237

    # 准备数据路径
    queryset_dir_path = f"txt_repo/testbody/query_set/{pro}"
    demopool_dir_path = f"txt_repo/testbody/demo_pool/{pro}"

    testunit_compile_stderr_dir_path = f"txt_repo/validation/{pro}/output/nonstop/testunit_compile"
    testunit_execute_stdout_dir_path = f"txt_repo/validation/{pro}/output/nonstop/testunit_execute"

    id_to_num_file = f"txt_repo/validation/{pro}/id_to_num.txt"
    overall_result_file = f"txt_repo/validation/{pro}/output/nonstop/overall_result.txt"
    passed_unit_file = f"txt_repo/validation/{pro}/output/nonstop/passed_test_unit.txt"
    check_chatgpt_file = f"txt_repo/validation/{pro}/output/nonstop/check_chatgpt.txt"
    compile_suc_and_execute_fail = f"txt_repo/validation/{pro}/output/nonstop/compile_suc_and_execute_fail_case.txt"

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
    testunit_compile_num = int(os.getenv("TESTUNIT_COMPILE_NUM"))
    testunit_execute_num = int(os.getenv("TESTUNIT_EXECUTE_NUM"))
    chatgpt_max_num = int(os.getenv("CHATGPT_MAX_NUM"))
    shot_num = int(os.getenv("SHOT_NUM"))

    # 读取queryset
    queryset = Testcase_Dataset(
        queryset_dir_path,
        "classname.txt",
        "constr_sign.txt",
        "focalname_paralist.txt",
        "test_name.txt",
        "fake_test_body.txt",
        "unixcoder_tensor.txt"
    )

    queryset_list = queryset.parse()
    assert len(queryset_list) == querynum_dict[pro]

    demopool = Testcase_Dataset(
        demopool_dir_path,
        "classname.txt",
        "constr_sign.txt",
        "focalname_paralist.txt",
        "test_name.txt",
        "test_body.txt",
        "unixcoder_tensor.txt"
    )

    try:
        result_datapoint_list = []
        # 进入循环
        end_idx = len(queryset_list)  # len(queryset_list)
        for id in range(start_idx, end_idx+1, 1):  #
            logger.info(f"💫来到第{id}个输入💫")

            result_datapoint = Result_datapoint(
                id, 0, 0, Test_Unit_Status.NONE_STATUS)
            tmp_query = queryset_list[id-1]

            tmp_demopool_list = demopool.parse(
                tmp_query.classname+tmp_query.focalname_paralist)

            candidate_demos, _ = testcase_diversity_retriever(
                tmp_query, tmp_demopool_list, shot_num)

            # generation stage
            logger.info('-'*10+" "+"generation stage"+" "+'-'*10)

            clear_chat_history()  # 当前query的首次调用，自然清空上一次的聊天记录

            return_testcase = ""
            prompt_for_gen = get_testbody_prompt(
                candidate_demos, tmp_query)

            for i in range(1, chatgpt_max_num, 1):  # retry外包状态码的问题，这里解决空值和不含代码的问题
                write_to_file(check_chatgpt_file,
                              f"generation stage 第{i}次调用chatgpt\n")
                return_testcase = call_chatgpt(prompt_for_gen)
                if return_testcase != "":  # 如果调用返回正常，就跳出循环
                    break
            return_testcase = fetch_method_chatgpt_out(return_testcase)
            return_testcase = form_complete_statement(return_testcase)
            write_to_file(check_chatgpt_file,
                          f"生成的testcase为：{return_testcase}  \n"+'-'*100 + '\n')

            test_unit = "public void " + \
                tmp_query.test_name + "{\n" + return_testcase + "\n}"

            write_to_file(check_chatgpt_file,
                          f"得到的test method为：\n{test_unit}  \n"+'-'*100 + '\n')

            # feedback stage
            logger.info('-'*10+" "+"feedback stage"+" "+'-'*10)
            clear_chat_history()  # 修复test_unit的编译错误 第2个清空聊天记录节点
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

            clear_chat_history()  # 修复test_unit的执行错误 第3个(also the last one)清空聊天记录节点
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
                logger.info(f"最终没能生成可执行的测试用例"+'\n'+'-'*100+'\n')
                result_datapoint.test_unit_status = Test_Unit_Status.COMPILE_SUCCESS_BUT_NOT_EXECUTE
                result_datapoint.compile_suc_execute_fail_unit = test_unit
            else:
                print(f"测试通过~~~"+'\n'+'-'*100+'\n')
                test_unit = test_unit.replace("\n", " ")
                result_datapoint.passed_test_unit = test_unit
                logger.info(
                    f"result_datapoint : {result_datapoint.toString()}")
                result_datapoint.test_unit_status = Test_Unit_Status.EXECUTE_SUCCESS
            result_datapoint_list.append(result_datapoint)

    except Exception as e:
        logger.info(f"main method got an exception: {e}")
    finally:
        for result_datapoint in result_datapoint_list:
            write_to_file(overall_result_file, result_datapoint.toString())

        # 现在是需要填论文表格的结果
        with open(id_to_num_file, "r") as f:
            id_to_num_list = f.readlines()
        bf_num, tf_num, passed_num = 0, 0, 0
        for result_datapoint in result_datapoint_list:
            now_id = result_datapoint.id
            status = result_datapoint.test_unit_status
            times = int(id_to_num_list[now_id-1])
            if status == Test_Unit_Status.NOT_COMPILE_SUCCESS:
                bf_num += times
            elif status == Test_Unit_Status.COMPILE_SUCCESS_BUT_NOT_EXECUTE:
                tf_num += times
                write_to_file(compile_suc_and_execute_fail,
                              str(result_datapoint.id)+", "+result_datapoint.compile_suc_execute_fail_unit+"\n")
            elif status == Test_Unit_Status.EXECUTE_SUCCESS:
                passed_num += times
                write_to_file(passed_unit_file,
                              str(result_datapoint.id)+", "+result_datapoint.passed_test_unit+"\n")
            else:
                raise Exception("出现了不应该出现的结果状态")

        # 最后把整体的情况写入到overall_output中
        # 打印整个项目的运行结果
        total_num = bf_num + tf_num + passed_num

        # 输出每种类型的绝对数量和所占比例
        percentage = (bf_num / total_num) * 100
        write_to_file(overall_result_file,
                      f"\n\nbuild failed : {bf_num} ({percentage:.2f}%) \n")
        percentage = (tf_num / total_num) * 100
        write_to_file(overall_result_file,
                      f"test failed : {tf_num} ({percentage:.2f}%) \n")
        percentage = (passed_num / total_num) * 100
        write_to_file(overall_result_file,
                      f"passed : {passed_num} ({percentage:.2f}%) \n")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"总耗时: {minutes} min {seconds} sec")
