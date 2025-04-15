TARGET_FILE_PATH = "txt_repo/mixed/csv/"

mixed_file_list = ["1_cn", "2_cs", "3_fcp", "4_fm",
                   "5_tn", "6_ti", "7_ora", "8_tm", "9_tb"]


for i in range(9):
    with open(TARGET_FILE_PATH+mixed_file_list[i]+".txt", "a") as tf:
        tf.write("--"*100+"\n")
