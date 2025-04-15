"""
File:create_test_name_file.py
Description:用于把被测方法的名字转化成测试用例的名字
Created Date:24.03.18
Last Updated Date:24.03.18
Usage:修改pro_name后点击运行
Input Files:txt_repo/langchain4j-prefix/query_set/pro_name/focalname_paralist.txt
Input Parameters:  
Output Files:txt_repo/langchain4j-prefix/query_set/pro_name/test_name.txt
Output Results:
"""

import re
from pathlib import Path

pro_name = 'qianfan'

# input_f = Path(f'txt_repo/langchain4j-prefix/query_set/{pro_name}/focalname_paralist.txt')
# output_f = Path(f'txt_repo/langchain4j-prefix/query_set/{pro_name}/test_name.txt')
tmp_input_f = Path(r'txt_repo\testbody\query_set\binance\focalname_paralist.txt')
tmp_output_f = Path(r'txt_repo\testbody\query_set\binance\test_name.txt')


def convert_to_test_method_name(java_method_name):
    """
    将Java方法名转换为对应的测试方法名。
    
    参数:
    - java_method_name: str, Java被测方法的名字，例如"toOpenAiMessages(List<ChatMessage> messages)"
    
    返回:
    - str, 对应的测试方法名，例如"testToOpenAiMessages"
    """
    # 使用正则表达式匹配Java方法名的开始部分，直到遇到左括号为止
    match = re.search(r"(\w+)\(", java_method_name)
    if match:
        # 获取匹配到的方法名
        method_name = match.group(1)
        # 将方法名的第一个字母转换为大写，并在前面添加"test"
        test_method_name = "test" + method_name[0].upper() + method_name[1:] + '()'
        return test_method_name
    else:
        # 如果没有匹配到任何内容，返回一个错误消息
        return "无法解析方法名"
    
def extract_funcname_from_signature(java_signature)->str:
    '''
    将Java参数签名转换为对应的测试方法名。
    '''
    # 使用空格分割签名以获取各个部分
    parts = java_signature.split()

    # 方法名通常紧跟在返回类型之后，因此找到第一个括号'('，然后向前找到方法名
    method_name = ""
    for part in parts:
        if '(' in part:
            method_name = part.split('(')[0]  # 移除括号和后面的参数部分
            break
    
    if not method_name:
        raise ValueError("Invalid Java signature provided")

    # 将方法名转换为测试方法名
    # 首字母大写，前面加上'test'
    test_method_name = 'test' + method_name[0].upper() + method_name[1:]+'()'
    
    return test_method_name

def main():
    with open(tmp_input_f,'r') as iif:
        input_lst = iif.readlines()
    with open(tmp_output_f,'w') as oof:
        for item in input_lst:
            if item.strip():
                if item.startswith('------------'):
                    oof.write(item)
                else:
                    tmn = extract_funcname_from_signature(item)
                    oof.write(tmn+'\n')

if __name__ == '__main__':
    main()