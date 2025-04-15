"""
File:infer_mutants.py
Description:根据变异日志的对变异的描述，推理出变异体
Created Date:24.1.8
Last Updated Date:24.1.9
Usage:图形界面点执行
Input Files:变异前的.java文件以及变异日志mutants.log
Input Parameters:NA  
Output Files:变异后的.java文件
Output Results:推理变异体这一过程成功与否
"""

import re
from pathlib import Path

mutants_log = Path("C:/Software/major/example/standalone/mutants.log")
source_code = Path("C:/Software/major/example/standalone/triangle/Triangle.java")
target_dir = Path("C:/Software/major/example/standalone/mutants")

def extract_mutation_info(mutants_log:Path):
    """
    提取出后面还原要用到的mutation信息：变异算子类型，变异前的组件，变异后的组件
    返回类型是一个List,其中每个元素是一个字典，字典的三个key分别是mutOp,mutate_line,source_comp,target_comp
    example 1:1:ROR:<=(int,int):<(int,int):triangle.Triangle@classify(int,int,int):14:a <= 0 |==> a < 0
    example 2:18:STD:<RETURN>:<NO-OP>:triangle.Triangle@classify(int,int,int):15:return TriangleType.INVALID; |==> <NO-OP>
    """
    mutation_info_list = []
    with open(mutants_log,'r') as f:
        for line in f:
            mutation_info = {}
            mutation_info['mutOp'] = line.split(':')[1]
            mutation_info['mutate_line'] = int(line.split(':')[-2])
            components = line.split(':')[-1]
            # 使用正则表达式匹配模式
            match = re.search(r'(.+?)\s*\|==>\s*(.+)', components)
            if match:
                mutation_info['source_comp'] = match.group(1).strip()
                mutation_info['target_comp'] = match.group(2).strip()
            else:
                raise Exception("Error: mutation log format error!")
            mutation_info_list.append(mutation_info)
    return mutation_info_list
    
def main():
    base_name = str(source_code).split('\\')[-1].split('.')[0] # get the class name
    mutation_info_list = extract_mutation_info(mutants_log)
    # print(f"将产生{len(mutation_info_list)}个变异体")
    source_code_lines = []
    with open(source_code,'r') as f:
        source_code_lines = f.readlines()
    for i,mutation_info in enumerate(mutation_info_list):
        # 从1开始计数
        mutant_id = i+1
        mutate_line = mutation_info['mutate_line']
        mutOp = mutation_info['mutOp']
        source_comp = mutation_info['source_comp']
        target_comp = mutation_info['target_comp']
        if source_code_lines[mutate_line-1].find(source_comp) == -1:
            raise Exception("Error: can't find source component!")
        if mutOp == 'STD' and target_comp != '<NO-OP>':
            raise Exception("Error: mutation log STD type error!")
        file_name = f"{base_name}_{mutant_id}.java"
        target_file = target_dir / file_name
        with open(target_file,'w') as f:
            for line in source_code_lines:
                if source_code_lines.index(line)+1 == mutate_line:
                    if mutOp == 'STD':
                        line = line.replace(source_comp,'')
                    else:
                        line = line.replace(source_comp,target_comp)
                f.write(line)

if __name__ == "__main__":
    main()