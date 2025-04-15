
vlis7_path_prefix = "/data2/chaoni/xiaoyawang/CodeX/"

sub_path = "txt_repo/mixed/lang/"

dir_name_list = [
    "class1_ArrayUtils_1f",
    "class2_BooleanUtils_64f",
    "class3_CharSequenceTranslator_1f",
    "class4_ClassUtils_1f",
    "class5_DateUtils_1f",
    "class6_DurationFormatUtils_1f",
    "class7_EqualsBuilder_64f",
    "class8_ExtendedMessageFormat_1f",
    "class9_FastDateFormat_64f",
    "class10_FastDateParser_1f",
    "class11_FastDatePrinter_1f",
    "class12_Fraction_64f",
    "class13_HashCoderBuilder_64f",
    "class14_LocaleUtils_64f",
    "class16_NumberUtils_64f",
    "class18_RandomStringUtils_1f",
    "class19_SerializationUtils_64f",
    "class20_StopWatch_64f",
    "class21_StrBuilder_1f",
    "class22_StringEscapeUtils_64f",
    "class23_StringUtils_1f",
    "class24_SystemUtils_64f",
    "class25_ToStringStyle_1f",
    "class26_TypeUtils_1f",
    "class28_WordUtils_64f"
]


def merge_files(file1, file2, output_file):  
    # 读取文件1的内容  
    with open(file1, 'r') as f1:  
        lines1 = f1.readlines()  
  
    # 读取文件2的内容  
    with open(file2, 'r') as f2:  
        lines2 = f2.readlines()  
  
    # 判断两个文件的行数是否相等  
    if len(lines1) != len(lines2):  
        print("Error: The number of lines in the two files is not equal.")  
        return  
  
    # 将文件1和文件2的内容进行拼接，用空格隔开，并写入输出文件  
    with open(output_file, 'w') as output_f:  
        for line1, line2 in zip(lines1, lines2):  
            merged_line = line1.strip() + ' ' + line2.strip() + '\n'  
            output_f.write(merged_line)  
  
    print("Merging completed successfully.") 


def main():
    for dir in dir_name_list:
        file1 = vlis7_path_prefix + sub_path + dir + "/6_ti.txt"
        file2 = vlis7_path_prefix + sub_path + dir + "/7_ora.txt"
        output_file = vlis7_path_prefix + sub_path + dir + "/9_tb.txt"
        merge_files(file1, file2, output_file)

if __name__ == '__main__':
    main()
