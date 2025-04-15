
SF = "ignore_it/check_repeat/lang/lang.txt"
TF = "ignore_it/check_repeat/lang/class_method.txt"


def extract_class_method(input_str):
    input_str = input_str.strip()
    idx_1 = input_str.find(" ")  # 第一个关键空格
    classname = input_str[:idx_1]
    idx_public = input_str.find("public")
    idx_2 = input_str.find(")", idx_public)  # 从public开始找，找到第一个)
    method_signature = input_str[idx_public+7:idx_2+1]

    return classname + " " + method_signature


def main():

    with open(SF, "r") as sf:
        sf = sf.readlines()
    with open(TF, "a") as tf:
        for i in range(0, len(sf)):
            line = sf[i]
            if line.startswith("---"):
                continue
            tf.write(extract_class_method(line)+"\n")


if __name__ == '__main__':
    main()
