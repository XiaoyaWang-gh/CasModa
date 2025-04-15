'''
gather_round_times.py
统计修复轮数，结果区间
(0,1,2,3,4,5)
'''
import os
import copy

from dotenv import load_dotenv
import logging
import json

from util.utils import read_to_list

validation_dir_path = "txt_repo\\validation"


def main():
    sample_order = "real_random"

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

    round_times_dict = {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    }

    all_round_times_dict = {pro: copy.copy(
        round_times_dict) for pro in pro_set}
    print(all_round_times_dict)

    for pro_name in pro_set:

        # logger.info(f"Here comes to 💎{pro_name}")
        overall_result_file = os.path.join(
            validation_dir_path, pro_name, "output", sample_order, "overall_result.txt")
        overall_result_list = read_to_list(overall_result_file)
        valid_line_num = num_dict[pro_name]
        overall_result_list = overall_result_list[:valid_line_num]

        id_to_num_file = os.path.join(
            validation_dir_path, pro_name, "id_to_num.txt")
        id_to_num_list = read_to_list(id_to_num_file)  # 每行just an int
        id_to_num_list = [int(i) for i in id_to_num_list]

        for result_item in overall_result_list:
            try:
                id, compile_round, execute_round, _ = result_item.split(", ")
                id = int(id)
                compile_round = int(compile_round)
                execute_round = int(execute_round)
                round_times = compile_round + execute_round - 2
                all_round_times_dict[pro_name][str(round_times)
                                               ] += id_to_num_list[id - 1]
            except Exception as e:
                print(result_item)

    # 各自打印和计算平均
    for pro, round_dict in all_round_times_dict.items():
        print(f"Here comes to 💎{pro}")
        print(round_dict)
        round_sum = 0
        for round_times, num in round_dict.items():
            round_sum += int(round_times) * num
        print(f"average round times: {(round_sum / num_dict[pro]):.3f}")
        print(sum(round_dict.values()))


if __name__ == "__main__":
    main()
