"""
File: 
    encapsulate_into_a_test_class.py
Description: 
    将同一个测试类的测试用例封装到那个类当中去，然后将一个project的所有类移动到对应的generated_by_chatgpt/下面
Date: 
    2023.10.08
Usage: 
    直接在图形界面运行
Input Files: 
    生成的测试方法文件(passed_test_unit.txt)，
    根据id将测试方法定位到测试类文件(evo_testClass_place.json)，
    测试类文件(test_class_plus_content/XXXTest.txt)
    根据项目名称和版本定位对应测试类目录(evo_pro_with_ver_to_test_place.json)
Input Parameters:  
    project_name: 项目名
    total_attempt_num: 总尝试次数(例如3，则封装attempt-1,attempt-2,attempt-3的测试方法)
Output Files: 
    某个pro的全部测试类文件
"""

from pathlib import Path
import json


def find_testclass_by_id(id, testClass_info_json_list):
    '''
    根据test method对应的id，找到对应的test class
    '''
    for obj in testClass_info_json_list:
        if id in obj.get("id_array"):
            return obj.get("test_class_name")


def insert_method_into_class(test_class, test_method, attempt_id, method_id):
    '''
    将test method插入到test class中，使用attempt_id和method_id修改test name
    输入：test class的内容，test_method的内容，attempt_id，method_id
    输出：插入test_method以及新占位符之后的的test class的内容
    '''
    # 修改test name(i.e.加上id)
    parentheses_idx = test_method.find("(")
    test_method = test_method[:parentheses_idx] + \
        f"_{attempt_id}_{method_id}" + test_method[parentheses_idx:]
    # 准备插入
    str_to_find = f"""@Test\n    <TestMethodPlaceHolder>"""
    insert_index = test_class.find(str_to_find)
    insert_suffix = "\n    "
    new_test_class = test_class[:insert_index] + \
        "@Test\n    "+test_method + insert_suffix + test_class[insert_index:]
    return new_test_class


def remove_redundant_placeholder(test_class):
    '''
    删除test class中多余的占位符
    '''
    str_to_find = f"""@Test\n    <TestMethodPlaceHolder>"""
    len_to_delete = len(str_to_find)
    delete_index = test_class.find(str_to_find)
    new_test_class = test_class[:delete_index] + \
        test_class[delete_index+len_to_delete:]
    return new_test_class


def main():
    # 确定Input Parameters
    project_name = "gson_plus"
    total_attempt_num = 6
    print(f"📢 现将{project_name}的{total_attempt_num}次生成的测试方法封装成测试类，用于和EvoSuite比较覆盖率")
    # 确定Input Files路径
    current_path = Path.cwd()
    test_methods_suffix = current_path / \
        f"txt_repo/validation/{project_name[:-5]}/output/evosuite"
    evo_testclass_place = current_path / \
        f"txt_repo/validation/{project_name[:-5]}/evo_testClass_place.json"
    pro_with_ver_to_test_place = current_path / \
        "txt_repo/validation/common/evo_pro_to_test_place.json"
    test_class_plus_suffix = current_path / \
        f"txt_repo/validation/{project_name[:-5]}/test_class_plus_content"
    # 将evo_testClass_place.json和evo_pro_with_ver_to_test_place.json转化为字典组成的list
    with open(evo_testclass_place, "r") as f:
        testClass_info = json.load(f)
    testClass_info_json_list = [dict(item) for item in testClass_info]
    with open(pro_with_ver_to_test_place, "r") as f:
        testPlace_info = json.load(f)
    testPlace_info_json_list = [dict(item) for item in testPlace_info]

    # 确定输出路径
    tmp_dir_name = f"total_{total_attempt_num}_attempts_test_classes"
    output_dir = test_methods_suffix / tmp_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    # 预备好写入输出文件的字典
    existed_test_class = dict()  # 每个item示例 test_class_name: test_class_content

    # 进入循环，封装每一个attempt的测试方法进测试类，写入字典existed_test_class
    for attempt_id in range(1, total_attempt_num+1):
        attempt_dir = f"attempt-{attempt_id}"
        # 找到具体的test_methods_file
        test_methods_file = test_methods_suffix / attempt_dir / "passed_test_unit.txt"

        with open(test_methods_file, 'r') as f:
            original_lines = f.readlines()
        for line in original_lines:
            print(f"📢第{attempt_id}批-读入的passed_test_unit单行内容是：\n{line}")
            method_id, test_method = line.split(",", maxsplit=1)
            method_id = int(method_id)  # int
            test_method = test_method.strip()  # str
            # 获取当前test method对应的test class
            test_class_name = find_testclass_by_id(
                method_id, testClass_info_json_list)
            # 若该test class已经存在于existed_test_class中
            if test_class_name in existed_test_class:
                # 则将该test method插入到该test class中，更新字典
                existed_test_class[test_class_name] = insert_method_into_class(
                    existed_test_class[test_class_name], test_method, attempt_id, method_id)
            # 若该test class不存在于existed_test_class中
            else:
                # 则新建一个key-value对
                # key: 从XXXTest.txt中读取
                with open(test_class_plus_suffix / f"{test_class_name}.txt", 'r') as f:
                    test_class = f.read()
                # value: 插入test method后的新test class
                existed_test_class[test_class_name] = insert_method_into_class(
                    test_class, test_method, attempt_id, method_id)

    # 将字典existed_test_class中的内容写入到文件中
    for test_class_name in existed_test_class:
        # 写入之前应当删除多余的占位符
        test_class_content = remove_redundant_placeholder(
            existed_test_class[test_class_name])
        # 删除<ID>
        test_class_content = test_class_content.replace("<ID>", "")

        output_file = output_dir / f"{test_class_name}.txt"
        output_file.touch()
        with open(output_file, 'w') as f:
            f.write(test_class_content)

    # 将output_dir下的所有文件从.txt后缀改为.java，移动到对应的generated_by_chatgpt(gbc_dir)下方
    # 首先找到对应的gbc_dir
    for pro_and_place in testPlace_info_json_list:
        if project_name == pro_and_place.get("pro"):
            gbc_dir = Path(pro_and_place.get("test_place"))
            break
    # 然后移动
    txt_generator = output_dir.glob("*.txt")
    for txt_file in txt_generator:
        # 把同名空白文件创建出来
        java_file = txt_file.with_suffix(".java")
        new_java_file = gbc_dir / java_file.name
        new_java_file.touch()
        # 填内容
        with open(txt_file, 'r') as f:
            java_content = f.read()
        with open(new_java_file, 'w') as f:
            f.write(java_content)


if __name__ == '__main__':
    main()
