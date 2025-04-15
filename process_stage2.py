# 该文件的目的是对阶段二的生成结果进行处理，处理如下
# (1)把没有以分号结尾的语句全部删除
# (2)把结束符END之后的内容删除
# (3)将注释手动删除

pro = "lang"
long_or_short = "short"  # "long" or "short
random_or_reverse = "random"

window_dict = {"long": "4097_text_window", "short": "3073_text_window"}
# 用一个字典保存每个项目的query数量
query_num_dict = {"gson":129,"cli":255,"csv":202,"chart": 989, "lang": 1215}

vlis7_path_prefix = "/data2/chaoni/xiaoyawang/CodeX/"
input_file = f"txt_repo/upd_scp_output/{pro}/3_oracle_stage/{window_dict[long_or_short]}/{random_or_reverse}/330_oracle_by_randomOrderDemos.txt"
output_file = f"txt_repo/upd_scp_output/{pro}/3_oracle_stage/{window_dict[long_or_short]}/{random_or_reverse}/330_oracle_by_randomOrderDemos_p.txt"

lines = []
with open(vlis7_path_prefix+input_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line.startswith("##"):
            lines.append(line)

assert len(lines) == query_num_dict[pro]

with open(vlis7_path_prefix+output_file, "a") as f:
    for i in range(len(lines)):
        line = lines[i]
        if not line.endswith(";"):
            semicolon_idx = line.rfind(";") # 从末尾开始找分号
            line = line[:semicolon_idx+1]
            print(f"第{i+1}条test oracle中含有未完成语句,已经删除")
        END_idx = line.find("END")
        if END_idx != -1:
            line = line[:END_idx]
            print(f"第{i+1}条test oracle中含有END,已经截断")
        if "//" in line:
            print(f"第{i+1}条test oracle中含有注释,请手动删除")
        if line == "":
            line = "return;"
        f.write(f"{line}\n")
        f.write(f"  ##ABOVE {i+1} th ##\n")
    