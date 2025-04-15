'''
source dir: 
    C:\codes\Java\extract_func_test_pair\src\main\java\org
files:
    funcTestMap.json
    funcClassMap.json
    funcSignMap.json
    classConstrMap.json
target dir: 
   - C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\testbody\demo_pool\binance
    C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\testbody\query_set\binance   
files:
    classname.txt
    constr_sign.txt
    focalname_paralist.txt
'''
import json
from pathlib import Path

source_dir = Path(r'C:\codes\Java\extract_func_test_pair\src\main\java\org')
target_dir = Path(r'C:\codes\CodeX\vlis7_backup\CodeX_back_to_chatgpt\txt_repo\testbody\query_set\binance')

def split_testcase(testcase: str) -> tuple[str, str]:
    '''
    Extracts the test method name and body from a Java unit test case string.

    :param testcase: Java unit test case as a string.
    :return: A tuple containing the test method name and the method body.
    '''
    # 查找方法名的开始位置
    start = testcase.find("public void")
    if start == -1:
        raise ValueError("No valid Java test case found")

    # 定位方法名结束位置（即第一个左括号）
    start_name = start + len("public void")
    end_name = testcase.find("(", start_name)

    if end_name == -1:
        raise ValueError("No method name found")

    # 提取方法名
    testname = testcase[start_name:end_name].strip() + "()"

    # 定位方法体的开始位置（即第一个左花括号）
    start_body = testcase.find("{", end_name)
    if start_body == -1:
        raise ValueError("No method body found")

    # 手动解析花括号以找到正确的结束位置
    brace_count = 1
    i = start_body + 1
    while i < len(testcase) and brace_count > 0:
        if testcase[i] == '{':
            brace_count += 1
        elif testcase[i] == '}':
            brace_count -= 1
        i += 1

    if brace_count != 0:
        raise ValueError("Mismatched braces in the Java test case")

    # 提取方法体
    testbody = testcase[start_body + 1:i - 1].strip()

    return testname, testbody

def main():
    # 最终写入3个file的数据量是一致的，取决于funcSignMap.json的数据量
    with open(source_dir/'funcClassMap.json','r') as f:
        func_class_map_json = json.load(f)
    func_class_map_dict = {item['funcname']:item['classname'] for item in func_class_map_json}
    print(len(func_class_map_dict))

    with open(source_dir/'funcSignMap.json','r') as f:
        func_sign_map_json = json.load(f)
    func_sign_map_dict = {item['funcname']:item['funcname_paralist'] for item in func_sign_map_json}
    print(len(func_sign_map_dict))

    with open(source_dir/'classConstrMap.json','r') as f:
        cls_constr_map_json = json.load(f)
    cls_constr_map_dict = {item['classname']:item['constructor'] for item in cls_constr_map_json}
    print(len(cls_constr_map_dict))

    for funcname in func_class_map_dict:
        funcsign = func_sign_map_dict[funcname]
        classname = func_class_map_dict[funcname]
        constructor = cls_constr_map_dict[classname]

        with open(target_dir/'focalname_paralist.txt','a') as f:
            f.write(funcsign+'\n')
        with open(target_dir/'classname.txt','a') as f:
            f.write(classname+'\n')
        with open(target_dir/'constr_sign.txt','a') as f:
            f.write(' '.join(constructor.splitlines())+'\n')


if __name__ == "__main__":
    main()