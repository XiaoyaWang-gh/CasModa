"""
File:extract_java_query_features.py
Description:使用javalang来解析Java代码，提取类名、构造函数名称、public方法的签名和完整代码
Created Date:24.03.14
Last Updated Date:24.03.14
Usage:提供API被主程序collect_entrance调用
Input Files: XXXX.java
Input Parameters: java文件所在路径
Output Files:
Output Results:
"""

import re
from typing import List,Dict,Union


def _remove_java_comments(code):
    # 删除所有多行注释
    code_without_multiline_comments = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # 删除所有单行注释
    code_without_any_comments = re.sub(r'//.*', '', code_without_multiline_comments)
    return code_without_any_comments

def _extract_java_info(java_code):
    # 提取类名
    class_name = re.findall(r'class (\w+)', java_code)[0]
    
    # 使用正则表达式匹配方法签名，包括跨行的参数列表
    # 注意：这里假设方法体是以 '{' 开始的，并且我们尽可能匹配到第一个出现的 ') {' 组合，考虑到可能的 throws 子句
    pattern = re.compile(r'public\s+(static\s+)?[^\s]+\s+(\w+\s*\([^\)]*\))\s*(throws [^\{]*?)?\{')
    public_method_signatures = pattern.findall(java_code)

    # 从匹配结果中提取方法签名
    signatures = [sig[1] for sig in public_method_signatures if not sig[1].startswith(class_name)]  # 排除构造函数

    return {
        'classname': class_name,
        'signatures': signatures,
    }

def _extract_method_bodies(java_code):
    # 匹配方法声明的正则表达式，包括返回类型、方法名和参数
    method_regex = re.compile(r'public\s+(static\s+)?([^\s]+)\s+(\w+)\s*\(([\s\S]*?)\)\s*(throws [\s\S]*?)?\{')
    methods = []

    for match in method_regex.finditer(java_code):
        start_index = match.end() - 1  # 获取"{"的位置，即方法体开始的地方
        open_brackets = 1  # 已经找到了方法体的起始大括号
        end_index = start_index

        # 遍历代码直到找到匹配的闭合大括号
        while open_brackets > 0 and end_index < len(java_code):
            end_index += 1
            if java_code[end_index] == '{':
                open_brackets += 1
            elif java_code[end_index] == '}':
                open_brackets -= 1
        
        # 截取并保存方法体
        methods.append(java_code[match.start():end_index+1])
    
    return methods

def extract_four_types_info(java_file_path)->Dict[str,Union[List,str,int]]:
    '''
    该方法调用上面三个方法
    '''
    info_dict = {
        'classname':'',
        'signatures':[],
        'methods':[],
        'met_num':0
    }

    with open(java_file_path,'r') as f:
        content = f.read()
    # 删除注释
    content = _remove_java_comments(content)
    # 调用函数
    info = _extract_java_info(content)
    methods = _extract_method_bodies(content)
    
    # 确保两个方法提取的public方法的个数是相同的
    if len(info['signatures']) != len(methods):
        print('❤'*20)
        print(java_file_path)
        print('❤'*20)
        raise Exception("Oops! Two extraction methods return different number of public methods!")
    
    # 确保两个方法提取的public方法的顺序是一致的
    for i in range(len(methods)):
        sig = info['signatures'][i]
        met = methods[i]
        if sig not in met:
            print('❤'*20)
            print(java_file_path)
            print('❤'*20)
            raise Exception('Two extraction methods seems return different orders!')

    info_dict['classname'] = info['classname']
    info_dict['signatures'] = info['signatures']
    info_dict['methods'] = methods
    info_dict['met_num'] = len(methods)

    return info_dict


def main():
    java_file_path = r"C:\dataset\trending_java_pros\langchain4j-0.28.0\langchain4j-qianfan\src\main\java\dev\langchain4j\model\qianfan\client\QianfanClient.java"
    info_dict = extract_four_types_info(java_file_path)
    print(info_dict['classname'])    
    print(info_dict['signatures'][0])    
    print(info_dict['methods'][0])    
    print(info_dict['met_num'])    

    

if __name__ == "__main__":
    main()