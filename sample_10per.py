# 此文件的目的是从每个项目中抽取出百分之十的数据，用于验证(4,3)修复组合
import os
import json
import random

from dotenv import load_dotenv

from util.utils import read_to_list

validation_dir_path = "txt_repo\\validation"


def find_combination(target_num, lst):
    '''
    函数的作用是从lst中选取若干个元素，使得他们的和等于(或者略小于)target_num
    参数
        target_num: 目标和
        lst: 备选数组
    返回值
        result: 一个数组，包含了选中元素的下标
    '''
    lst_len = len(lst)
    step = lst_len // 10
    index = 1
    index_lst = []
    practical_num = 0

    # 3是一个经验值，不加得到的value_lst总比target_num小3-4
    # 3 -> 2
    while practical_num + lst[index] < target_num + 2:
        practical_num += lst[index]
        index_lst.append(index)
        index += step
        index = index % lst_len

    return index_lst


def main():
    load_dotenv()
    pro_str = os.getenv("PRO_SET")
    pro_set = json.loads(pro_str)

    # 读取QUERYNUM_DUP_DICT，知道百分之十是多少
    num_str = os.getenv("QUERYNUM_DUP_DICT")
    tmp_dict = json.loads(num_str)
    num_dict = {key: int(value) for key, value in tmp_dict.items()}

    for pro in pro_set:
        print(f"Here comes to 💎{pro}")
        # 去到txt_repo validation每个项目下面的id_to_num中，选出这1/10，存入外部文件sample.json中
        id_to_num_file = os.path.join(
            validation_dir_path, pro, "id_to_num.txt")
        id_to_num_list = read_to_list(id_to_num_file)  # 每行just an int
        id_to_num_list = [int(i) for i in id_to_num_list]

        target_num = num_dict[pro] // 10
        print(f"target_num : {target_num}")
        id_lst = find_combination(target_num, id_to_num_list)
        print(f"id_lst : {id_lst}")
        value_lst = [id_to_num_list[i] for i in id_lst]
        print(f"value_lst : {value_lst}\n\n")

    # 修改CUTE_pileline，依据sample.json得到结果

    # 我要一次把这个程序写完，不要手动执行五次，做不到


if __name__ == "__main__":
    main()
