import os

PREFIX_OR_ORACLE = "oracle"

source_dir = "C:/codes/CodeX/CodeX/txt_repo/mixed/chart"
target_dir = f"C:/codes/CodeX/CodeX/txt_repo/{PREFIX_OR_ORACLE}/demo_pool/chart"


def varification():
    dir_list = os.listdir(source_dir)
    for dir in dir_list:
        file_list = os.listdir(os.path.join(source_dir, dir))
        for file in file_list:
            with open(os.path.join(source_dir, dir, file), "r", encoding='utf-8') as f:
                lines = f.readlines()
                print(f"{dir} {file} {len(lines)}")


def count_datanum_each_class():
    dir_list = os.listdir(source_dir)
    dir_list.sort()
    for dir in dir_list:
        file_list = os.listdir(os.path.join(source_dir, dir))
        with open(os.path.join(source_dir, dir, file_list[0])) as file_cn:
            print(f"{dir} {len(file_cn.readlines())}")


'''
对应关系
1_cn.txt -> classname.txt
2_cs.txt -> constr_sign.txt
3_fcp.txt -> focalname_paralist.txt
4_fm.txt -> focal_method.txt
5_tn.txt -> testname.txt
6_ti.txt -> test_input.txt
'''


def write_to_demopool():
    if PREFIX_OR_ORACLE == "prefix":
        sf = ["1_cn.txt", "2_cs.txt", "3_fcp.txt",
              "4_fm.txt", "5_tn.txt", "6_ti.txt"]
        tf = ["classname.txt", "constr_sign.txt", "focalname_paralist.txt",
              "focal_method.txt", "testname.txt", "test_input.txt"]
    elif PREFIX_OR_ORACLE == "oracle":
        sf = ["3_fcp.txt", "4_fm.txt", "5_tn.txt", "7_ora.txt", "8_tm.txt"]
        tf = ["focalname_paralist.txt", "focal_method.txt",
              "test_name.txt", "oracle.txt", "test_method.txt"]

    for i in range(len(tf)):  # 外层循环 - 6个文件
        with open(os.path.join(target_dir, tf[i]), "a", encoding='utf-8') as tFile:
            # 逐个打开source_dir下面的文件夹
            for dir in os.listdir(source_dir):  # 内层循环 - 24个类
                with open(os.path.join(source_dir, dir, sf[i]), "r", encoding='utf-8') as sFile:
                    lines = sFile.readlines()
                    for line in lines:
                        tFile.write(line)
                tFile.write('-'*150+"\n")


def main():
    # 三件事
    # 1. 确保source_dir下面24个以class开头的文件夹下面的9个文件中数据的条目相同
    # 2. 输入每个class下面的数据条数
    # 3. 将source_dir下面相应文件写入target_dir,不同类之间用分隔符隔开
    write_to_demopool()


if __name__ == "__main__":
    main()
