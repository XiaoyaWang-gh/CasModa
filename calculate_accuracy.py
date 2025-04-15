'''
calculate_accuracy.py
此脚本的作用是检验passed_test_unit当中有哪些是没有调用被测方法的，即false positive

'''
import os
import sys
import json
from dotenv import load_dotenv
import logging

from util.utils import read_to_list

validation_dir_path = "txt_repo\\validation"


def if_call(focalname, test_unit):
    '''
    用来判断某个测试用例是否真的调用了某个被测方法
    :param focalname: 被测方法的名字
    :param test_unit: 测试用例的名字
    :return: True or False
    '''
    focalname_wo_param = focalname.split("(")[0]

    # 必要条件1：测试用例的方法体中包含被测方法的名字
    if focalname_wo_param in test_unit:
        # 必要条件2：参数个数也一致
        # 获取被测方法的参数个数
        focal_param_num = focalname.count(",") + 1
        # 获取测试用例中“调用方法”的参数个数
        start_idx = test_unit.find(
            focalname_wo_param) + len(focalname_wo_param)
        end_idx = test_unit.find(")", start_idx)
        method_num = test_unit[start_idx:end_idx].count(",") + 1

        if focal_param_num == method_num:
            return True
        else:
            return False


def main():
    # 设置一个logger，取代导出散落的print
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 加载该加载的变量
    load_dotenv()
    pro_name = "gson"
    res_type = "swap_pool"

    # num_str = os.getenv("QUERYNUM_DUP_DICT")
    # tmp_dict = json.loads(num_str)
    # num_dict = {key: int(value) for key, value in tmp_dict.items()}

    id_to_num_file = os.path.join(
        validation_dir_path, pro_name, "id_to_num.txt")
    focalname_file = os.path.join(
        "txt_repo\\prefix\\query_set", pro_name, "focalname_paralist.txt")
    passed_unit_file = os.path.join(
        validation_dir_path, pro_name, "output", res_type, "passed_test_unit.txt")

    id_to_num_list = read_to_list(id_to_num_file)  # 每行just an int
    # 每行包括 just focalname + paralist
    focalname_list = read_to_list(focalname_file)
    passed_unit_list = read_to_list(passed_unit_file)  # 每行是int + , + test_unit

    assert len(id_to_num_list) == len(focalname_list)

    # 将id_to_num_list转化成一个字典，方便查每个id对应的数量
    id_num_map = dict()
    
    for i, num in enumerate(id_to_num_list):
        id = i + 1
        id_num_map[id] = int(num)

    # 将focalname_list转化成一个字典，方便查每个id对应的focalname
    id_focalname_map = dict()
    for i, focalname in enumerate(focalname_list):
        id = i + 1
        id_focalname_map[id] = focalname

    # 对于passed_unit_list中的每一行，需要将其拆分为id和test_unit, 同样存入字典中
    id_testunit_map = dict()
    for line in passed_unit_list:
        id, test_unit = line.split(",", 1)
        test_unit = test_unit.strip()
        id_testunit_map[int(id)] = test_unit

    # 开始逐个验证
    total_num = 0
    correct_num = 0
    for id, test_unit in id_testunit_map.items():
        times = id_num_map[id]
        total_num += times
        focalname = id_focalname_map[id]
        if if_call(focalname, test_unit):
            correct_num += times

    print("correct_num is : ", correct_num)
    print("total_num is : ", total_num)
    print("accuracy is : ", "{:.2%}".format(correct_num / total_num))


if __name__ == "__main__":
    main()
