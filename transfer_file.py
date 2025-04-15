import os

pname = "cli"
queryset_or_demopool = "demo_pool"  # query_set demo_pool

strengthened_class_path_num_dict = {
    "class3_DefaultParser_v1.5/": 20,
    "class4_GroupImpl_v2.0/": 48,
    "class5_HelpFormatter_v1.5/": 80,
    "class7_OptionBuilder_v1.5/": 70,
    "class11_Parser_v1.1/": 16,
    "class15_WriteableCommandLineImpl_v2.0/": 40,
    "original_allclass/": 228
}

# 定义路径
path = f"txt_repo/mixed/{pname}/"

sub_path = f"txt_repo/testbody/{queryset_or_demopool}/{pname}/"
file_names = ["1_cn.txt", "2_cs.txt", "3_fcp.txt",
              "5_tn.txt", "9_tb.txt"]
sub_file_names = ["classname.txt", "constr_sign.txt",
                  "focalname_paralist.txt", "test_name.txt", "test_body.txt"]


# 创建目录
os.makedirs(path, exist_ok=True)


# 写入文件

def finish_one_class_transfer(classname: str, added_line_num: int):
    cnt = 0
    for file, sub_file in zip(file_names, sub_file_names):
        with open(path+classname+file, "r", encoding='utf-8', errors='ignore') as rf:
            print(f"正在处理{classname}...")
            content = rf.readlines()
            with open(sub_path+sub_file, "a") as af:
                af.write('--'*100+"\n")
                for i in range(len(content)-added_line_num, len(content)):
                    af.write(content[i])
                print(f"{sub_file}文件新增{added_line_num}行数据")
            with open(sub_path+sub_file, "r") as rf_:
                print(f"{sub_file}文件当前行数为{len(rf_.readlines())}")

        cnt += 1

    print(f"{cnt}个文件已创建完成！")


def main():
    for class_name, added_line_num in strengthened_class_path_num_dict.items():
        finish_one_class_transfer(class_name, added_line_num)


if __name__ == '__main__':
    main()
