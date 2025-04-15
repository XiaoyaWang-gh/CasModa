'''
calculate_coverage.py
24.03.22进行修改，使得能针对单个项目id不全的passed_test_unit.txt进行评估

'''

import os
import sys

from dotenv import load_dotenv
import logging
import json

from util.utils import read_to_list
from calculate_accuracy import if_call

validation_dir_path = "txt_repo\\validation"


def main():
    # 设置一个logger，取代导出散落的print
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    pro_name = "gson"
    res_type = "swap_pool"

    logger.info(f"Here comes to 💎{pro_name}")
    # 获取文件
    id_to_num_file = os.path.join(
        validation_dir_path, pro_name, "id_to_num.txt")
    focalname_file = os.path.join(
        "txt_repo\\prefix\\query_set", pro_name, "focalname_paralist.txt")
    passed_unit_file = os.path.join(
        validation_dir_path, pro_name, "output", res_type, "passed_test_unit.txt")

    # step 1 完成当前项目数目字典的构建focalme_num_dict，即哪个focal method对应的num
    id_to_num_list = read_to_list(id_to_num_file)  # 每行just an int
    id_to_num_list = [int(i) for i in id_to_num_list]
    # 每行包括 just focalname + paralist
    focalname_list = read_to_list(focalname_file)
    passed_unit_list = read_to_list(
        passed_unit_file)  # 每行是int + , + test_unit

    assert len(id_to_num_list) == len(focalname_list)
    # 初始值全为0，如果被测到改为1
    tested_hashtable = [0] * 3000

    focalme_num_dict = {focalname: id_to_num for focalname,
                        id_to_num in zip(focalname_list, id_to_num_list)}

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

    # 记录哪些id的focal method被用于生成测试用例，初始全为0，被选中改为1
    try_hashmap = [0] * 1000 
    # step 2 遍历passed_unit_list，如果在字典中，那么加上对应的数目
    for line in passed_unit_list:
        id, test_unit = line.split(",", 1)
        id = int(id)
        try_hashmap[id] = 1
        test_unit = test_unit.strip()
        # 先看对应的有没有测到
        if if_call(id_focalname_map.get(id), test_unit) and tested_hashtable[id] == 0:
            tested_hashtable[id] = 1
            continue
        for focalname in focalme_num_dict:  # 如果上一个答案是否定的，再看看其他的有没有测到
            if if_call(focalname, test_unit) and tested_hashtable[id] == 0:
                tested_hashtable[id] = 1
                break

    # step 3 focal method coverage
    try_num = 0
    for id in range(1,len(try_hashmap)):
        if try_hashmap[id] == 1:
            try_num += id_num_map[id]
    tested_num = 0
    for id in range(1,len(tested_hashtable)):
        if tested_hashtable[id] == 1:
            tested_num += id_num_map[id]

    focalme_coverage = tested_num / try_num
    percentage = "{:.2%}".format(focalme_coverage)
    print(f"📍{pro_name} focalme_coverage: {percentage}")


if __name__ == "__main__":
    main()
