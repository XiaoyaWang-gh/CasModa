"""
File:correct_test_name_file.py
Description:之前测试用例的名字忘记结尾加括号了
Created Date:24.03.19
Last Updated Date:24.03.19
Usage:修改pro_name后点击运行
Input Files:txt_repo/langchain4j-prefix/query_set/pro_name/test_name.txt
Input Parameters:  
Output Files:txt_repo/langchain4j-prefix/query_set/pro_name/test_name_.txt
Output Results:
"""

import re
from pathlib import Path

pro_name = 'core'

input_f = Path(f'txt_repo/langchain4j-prefix/query_set/{pro_name}/test_name.txt')
output_f = Path(f'txt_repo/langchain4j-prefix/query_set/{pro_name}/test_name_.txt')
    

def main():
    with open(input_f,'r') as iif:
        input_lst = iif.readlines()
    with open(output_f,'w') as oof:
        for item in input_lst:
            if item.strip():
                if item.startswith('------------'):
                    oof.write(item)
                else:
                    oof.write(item.strip()+'()\n')

if __name__ == '__main__':
    main()