import time
import os
import json
import sys
import re
from mytemplate.bf_repair_template import compile_failed_repair_template
from mytemplate.tf_repair_template import test_failed_repair_template
from CUTE_components.models import Failed_To_Be_Repair_datapoint
from chatgpt_api.codex_api_proxy import ChatGPTAPI

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


'''
step 1 获取编译失败和测试失败的id_list，以及对应的被测类类名、构造器、被测方法名，构建修复阶段的prompt (先只考虑修复一次)
step 2 调用chatgpt生成新的结果
step 3 验证新生成的结果是否通过测试
'''

# step 1 获取编译失败和测试失败的id_list，以及对应的被测类类名、构造器、被测方法名，构建修复阶段的prompt (先只考虑修复一次)
# details
pro_name = "cli"
shot_num = 5
order = "reverse"

failed_list_file = f"txt_repo/validation/{pro_name}/output/shot_{shot_num}/{order}/overall.txt"

classname_file = f"txt_repo/prefix/query_set/{pro_name}/classname.txt"
focalname_paralist_file = f"txt_repo/prefix/query_set/{pro_name}/focalname_paralist.txt"
test_unit_file = f"txt_repo/gpt_output/{pro_name}/4_final_stage/shot_{shot_num}/{order}/CUTE_testCase.txt"

validate_output_path = f"txt_repo/validation/{pro_name}/output/shot_{shot_num}/{order}"
test_class_place_path = f"txt_repo/validation/{pro_name}/testClass_place.json"


# step 2 调用chatgpt生成新的结果
# detail-1 使用utils.py中的extract_code_snippet_from_chatgpt方法提取代码片段
bf_repair_result_file = f"txt_repo/validation/{pro_name}/output/shot_{shot_num}/{order}/bf_repair_output.txt"
tf_repair_result_file = f"txt_repo/validation/{pro_name}/output/shot_{shot_num}/{order}/tf_repair_output.txt"


# step 3 验证新生成的结果是否通过测试


# 从本行开始都是工具函数
def extract_id_list(filename, keyword):
    with open(filename, 'r') as file:
        content = file.readlines()

    for line in content:
        if line.startswith(keyword):
            id_list = line[len(keyword):].strip().split()
            break

    # 将列表中的元素转换为整数类型
    id_list = list(map(int, id_list))

    return id_list


def get_test_class_name(json_file_path, id):
    with open(json_file_path) as f:
        data = json.load(f)

    for obj in data:
        id_array = obj['id_array']
        if id in id_array:
            return obj['test_class_name']


def extract_stderr_message(input_string):
    # 删除 ^
    tmp_string = input_string.replace("^", "")
    # 删除 stdout:
    tmp_string = tmp_string.replace("stdout:", "")
    # 连续空格换成单个空格
    tmp_string = re.sub(r'[ \t]+', ' ', tmp_string)
    # 删除文件路径
    output_string = re.sub(
        r'[A-Za-z]:\\.*?java:\d+:', '', tmp_string)
    # 删除空白行
    output_string = re.sub(r'\n\s*\n', '\n', output_string)

    return output_string


def extract_stdout_message(input_string):
    # 正则表达式模式，匹配以 "There was 1 failure:" 开始，以 "FAILURES!!!" 结束之间的内容
    pattern = r"There (was|were) \d+ failure(s):(.*?)FAILURES!!!"
    match = re.search(pattern, input_string, re.DOTALL)

    if match:
        # 提取匹配结果中的内容
        extracted_message = match.group(1).strip()
        return extracted_message
    else:
        return input_string


def call_chatgpt(output_file, prompt):
    codex = ChatGPTAPI(output_file)
    codex.get_suggestions(prompt, True)


def main():
    compile_failed_id_list = extract_id_list(
        failed_list_file, "compile_failed_id_list : ")
    test_failed_id_list = extract_id_list(
        failed_list_file, "test_failed_id_list : ")

    classname_list, focalname_paralist_list, test_unit_list = [], [], []
    with open(classname_file, 'r') as file:
        for line in file:
            classname_list.append(line.strip())
    with open(focalname_paralist_file, 'r') as file:
        for line in file:
            focalname_paralist_list.append(line.strip())
    with open(test_unit_file, 'r') as file:
        for line in file:
            test_unit_list.append(line.strip())

    # 对于编译错误的
    for idx in range(0, 1, 1):  # len(compile_failed_id_list)
        id = compile_failed_id_list[idx]
        classname = classname_list[id-1]
        focalname_paralist = focalname_paralist_list[id-1]
        test_unit = test_unit_list[id-1]
        stderr_name = get_test_class_name(test_class_place_path, id)
        stderr_file = os.path.join(
            validate_output_path, "compile_failed", stderr_name+str(id)+".txt")
        stderr_content = ""
        with open(stderr_file, 'r', encoding="utf-8") as file:
            stderr_content = extract_stderr_message(file.read())
        bf_datapoint = Failed_To_Be_Repair_datapoint(
            classname, focalname_paralist, stderr_content, test_unit)
        repair_prompt = compile_failed_repair_template(bf_datapoint)
        call_chatgpt(bf_repair_result_file, repair_prompt)
        with open(bf_repair_result_file, "a", encoding="utf-8") as file:
            file.write(f"\n## ABOVE {stderr_name}{id}\n")

    # 对于运行时错误的
    for idx in range(0, 1, 1):  # len(test_failed_id_list)
        id = test_failed_id_list[idx]
        classname = classname_list[id-1]
        focalname_paralist = focalname_paralist_list[id-1]
        test_unit = test_unit_list[id-1]
        stdout_name = get_test_class_name(test_class_place_path, id)
        stdout_file = os.path.join(
            validate_output_path, "test_failed", stdout_name+str(id)+".txt")
        stdout_content = ""
        with open(stdout_file, 'r', encoding="utf-8") as file:
            stdout_content = extract_stdout_message(file.read())
        tf_datapoint = Failed_To_Be_Repair_datapoint(classname, focalname_paralist,
                                                     stdout_content, test_unit)
        repair_prompt = test_failed_repair_template(tf_datapoint)
        call_chatgpt(tf_repair_result_file, repair_prompt)
        with open(tf_repair_result_file, "a", encoding="utf-8") as file:
            file.write(f"\n## ABOVE {stdout_name}{id}\n")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"总耗时: {minutes} min {seconds} sec")
