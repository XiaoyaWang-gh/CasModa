path_prefix = "/data2/chaoni/xiaoyawang/CodeX/txt_repo/upd_scp_output/"

# 以下三个变量每次运行需要填写
pname = "csv"
text_window_type = "long" # "long" or "short"
stage_type = "stage1" # "stage1" or "stage2"

window_dict = {"long": "4097_text_window/", "short": "2049_text_window/"}
stage_dict = {"stage1": "demonumber_when_testInput_randomOrder.txt", "stage2": "demonumber_genStage2_randomOrder.txt"}

final_path = path_prefix + pname + "/5_demo_number/" + window_dict[text_window_type] + stage_dict[stage_type]


with open(final_path, "r") as f:
    demo_num_list = f.readlines()
    # 求平均值
    demo_num_list = [int(x.strip()) for x in demo_num_list]
    print(f"💚💙🧡 {pname} {stage_type}: average demo number: ", sum(demo_num_list) / len(demo_num_list))