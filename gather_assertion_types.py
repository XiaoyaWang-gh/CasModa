# 对于每个生成结果文件，统计其包含的断言类型
# 第一类是粗略统计，即有positive v.s. negative
# 第二类是细致统计，即有assertEquals v.s. assertTrue v.s. assertThat

# 主要手段是基于字符串匹配
# 1. positive: assertTrue(, assertEquals(, assertThat(, assertSame(, assertNotSame(
# 2. negative: assertThrows(, expect(


import os
import copy

from dotenv import load_dotenv
import logging
import json

from util.utils import read_to_list

validation_dir_path = "txt_repo\\validation"


POSITIVE_ASSERT_LST = ["assertEquals", "assertNotEquals", "assertTrue", "assertFalse",
                       "assertNull", "assertNotNull", "assertSame", "assertNotSame",
                       "assertArrayEquals", "assertThat"]
NEGATIVE_ASSERT_LST = ["assertThrows", "expect", "fail"]


def get_test_unit_type(test_unit: str):
    '''
    test_unit: str 传入字符串形式的测试用例
    return: str 返回测试用例的类型，positive, negative, mixed, none
    positive 代表只有正向断言
    negative 代表只有负向断言
    mixed 代表正负断言都有
    none 代表没有断言(可能是2个assert_lst以外的断言)
    '''
    p_flag = False
    n_flag = False
    if any(assertion in test_unit for assertion in POSITIVE_ASSERT_LST):
        p_flag = True
    if any(assertion in test_unit for assertion in NEGATIVE_ASSERT_LST):
        n_flag = True

    test_type = "none"
    if p_flag and n_flag:
        return "mixed"
    elif p_flag and not n_flag:
        return "positive"
    elif not p_flag and n_flag:
        return "negative"

    return test_type


def get_assert_dict(test_unit: str):
    '''
    test_unit: str 传入字符串形式的测试用例
    return: dict like {"assertEquals": 2, "assertTrue": 1}
    '''
    all_assert_list = POSITIVE_ASSERT_LST + NEGATIVE_ASSERT_LST
    tmp_dict = {key: 0 for key in all_assert_list}
    for assertion in all_assert_list:
        tmp_dict[assertion] = test_unit.count(assertion)
    # 移除所有value为0的item
    assert_dict = {key: value for key, value in tmp_dict.items() if value != 0}
    return assert_dict


def add_dicts(dict1, dict2):
    """  
    将两个字典中相同键的值相加，并返回一个新的字典。  

    参数：  
        dict1 (dict): 第一个字典。  
        dict2 (dict): 第二个字典。  

    返回：  
        dict: 合并后的字典，包含两个字典中相同键的值相加的结果。  

    示例：  
        dict_1 = {'a': 1, 'b': 2, 'c': 0, 'd': 4}  
        dict_2 = {'a': 4}  
        merged_dict = add_dicts(dict_1, dict_2)  
        print(merged_dict)  
        # 输出: {'a': 5, 'b': 2, 'c': 0, 'd': 4}  
    """
    result_dict = dict(dict1)  # 创建一个新字典，初始值为dict1的副本
    for key, value in dict2.items():
        if key in result_dict:
            result_dict[key] += value
        else:
            result_dict[key] = value
    return result_dict


def main():
    sample_order = "random"

    # 设置一个logger，取代到处散落的print
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # 加载该加载的变量
    load_dotenv()
    pro_str = os.getenv("PRO_SET")
    pro_set = json.loads(pro_str)
    num_str = os.getenv("QUERYNUM_DUP_DICT")
    tmp_dict = json.loads(num_str)
    num_dict = {key: int(value) for key, value in tmp_dict.items()}

    for pro_name in pro_set:

        logger.info(f"Here comes to 💎{pro_name}")
        passed_test_unit_file = os.path.join(
            validation_dir_path, pro_name, "output", sample_order, "passed_test_unit.txt")
        passed_test_unit_list = read_to_list(passed_test_unit_file)
        valid_line_num = num_dict[pro_name]
        passed_test_unit_list = passed_test_unit_list[:valid_line_num]

        id_to_num_file = os.path.join(
            validation_dir_path, pro_name, "id_to_num.txt")
        id_to_num_list = read_to_list(id_to_num_file)  # 每行just an int
        id_to_num_list = [int(i) for i in id_to_num_list]

        test_unit_type_dict = {
            "positive": 0,
            "negative": 0,
            "mixed": 0,
            "none": 0
        }

        test_assertion_dict = {
            key: 0 for key in POSITIVE_ASSERT_LST+NEGATIVE_ASSERT_LST}

        for list_item in passed_test_unit_list:
            try:
                id, test_unit = list_item.split(",", 1)
                id = int(id)
                test_unit = test_unit.strip()
                # 首先确定test_unit的总类型
                test_unit_type = get_test_unit_type(test_unit)
                test_unit_type_dict[test_unit_type] += id_to_num_list[id-1]
                # 其次确定test_unit的包含的具体assertion类型
                assert_dict = get_assert_dict(test_unit)
                for _ in range(id_to_num_list[id-1]):
                    test_assertion_dict = add_dicts(
                        test_assertion_dict, assert_dict)

            except Exception as e:
                print(list_item)
                print(str(e))

        print(test_unit_type_dict)
        print(test_assertion_dict)


if __name__ == "__main__":
    main()
