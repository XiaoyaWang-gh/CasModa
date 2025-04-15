import autopep8

DIR = "txt_repo/output/prefix_stage/"
sFILE = "testInput_by_forwardOrderDemos.txt"
tFILE = "clean_testInput_by_forwardOrderDemos.txt"


'''
本方法需要达到以下目的:
1. 检测第一阶段的生成结果，将符合语法的结果写进clean_testInput_xxx.txt，不符合则跳过
2. 遇到分隔符行 同样写入clean_testInput_xxx.txt
'''


def check_testInput():

    # 打开目标文件
    tf = open(DIR + sFILE, "a")

    # 逐行读取文件
    with open(DIR + tFILE, "r") as sf:
        # 逐行读取
        for line in sf:
            line = line.strip()
            if line.startswith("##"):  # 如果是分隔符行，直接写入
                tf.write(line+"\n")
            else:
                if line.endswith(";"):  # 如果以分号结尾，语法有了一定保障，也写入
                    tf.write(line+"\n")

    # 关闭目标文件
    tf.close()


def main():
    check_testInput()


if __name__ == "__main__":
    main()
