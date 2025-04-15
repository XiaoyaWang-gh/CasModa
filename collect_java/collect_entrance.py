"""
File: collect_entrance.py
Description:处理单元是一整个pro，对于java_file_paths中存储的每个类的路径逐个地调用解析函数，提取出类名，public方法名+参数列表，public方法全部代码
Created Date:23.03.14
Last Updated Date:23.03.15
Usage:python -m collect_entrance pro_name
Input Files:java_file_paths.txt
Input Parameters:pro_name
Output Files:classname.txt,focalname_paralist.txt,focal_method.txt
Output Results:num_of_classes(c_cnt),num_of_methods(m_cnt)
"""
import sys
from pathlib import Path
from extract_java_query_features import extract_four_types_info



def main(pro_name):
    
    path_of_paths = Path(f'{pro_name}/java_file_paths.txt')
    with open(path_of_paths,'r') as f:
        paths = f.readlines()
        paths = [path.strip() for path in paths]

    # 开始把信息写入存储文件夹
    root_collect_path = Path(f'{pro_name}/collected_info/')
    cn_path = root_collect_path / "classname.txt"
    fp_path = root_collect_path / "focalname_paralist.txt"
    fm_path = root_collect_path / "focal_method.txt"

    m_cnt = 0
    for p in paths:
        info_dict = extract_four_types_info(p)
        classname = info_dict['classname']
        met_num = info_dict['met_num']
        m_cnt += met_num
        print(classname)       
        print(met_num)  
        print('-'*50)
        with open(cn_path,'a') as f:
            for _ in range(met_num):
                f.write(classname+'\n')
            f.write('-'*100+'\n')
        with open(fp_path,'a') as f:
            for fp in info_dict['signatures']:
                fp = fp.replace('\n','')
                fp = fp.strip()
                f.write(fp+'\n')
            f.write('-'*100+'\n')
        with open(fm_path,'a') as f:
            for fm in info_dict['methods']:
                fm = fm.replace('\n','')
                fm = fm.strip()
                f.write(fm+'\n')
            f.write('-'*100+'\n')
    
    c_cnt = len(paths)

    print(
        f"{pro_name} has collected {c_cnt} classes and {m_cnt} methods."
    )


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        pro_name = sys.argv[1]
    else:
        raise Exception('Usage : python -m collect_entrance pro_name')
    main(pro_name)