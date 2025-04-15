import os

pname = "lang"

SOURCE_FILE = f"C:/dataset/d4j-spec5/A3Test provided/{pname}/sorted_{pname}.txt"
TARGET_FILE = f"C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/{pname}/focal_method.txt"


# get focal method from original txt file
def get_fm():
    # 读取source文件
    with open(SOURCE_FILE, "r") as sf:
        flag = 1
        for line in sf:
            if line.startswith("---"):
                # 读取target文件
                with open(TARGET_FILE, "a") as tf:
                    # write 100 '-' into tf
                    tf.write("--"*100)
                    tf.write("\n")
            else:
                # 截取从public开始到第一个}结束的字符串
                # locate the first "public"
                start = line.find("public")
                # locate the first "}" after "public"
                tmp_end = line.find("}", start)
                if line.find("{", tmp_end) > 0:
                    first_l = line.find("{")
                    if not os.path.exists(TARGET_FILE):
                        open(TARGET_FILE, "w+").close()
                    with open(TARGET_FILE, "a") as tf:
                        tf.write("$$")
                        tf.write(line[first_l+1:-1])
                        tf.write("\n")
                else:
                    # count the number of "{" between start and tmp_end
                    count = line.count("{", start, tmp_end+1)
                    if count == 0:
                        # 没有方法体的方法不如手动补上
                        if not os.path.exists(TARGET_FILE):
                            open(TARGET_FILE, "w+").close()
                        with open(TARGET_FILE, "a") as tf:
                            tf.write(
                                "$$$ Please mannally collect the method as it has no method body\n")
                    else:
                        # locate the count_th "}" after the last "{" between start and tmp_end
                        i = 1
                        while i < count:
                            tmp_end = line.find("}", tmp_end+1)
                            i += 1
                        assert count == i
                        end = tmp_end
                        # 截取substr从start到end
                        new_line = line[start:end+1]
                        # write new_line into tf
                        if not os.path.exists(TARGET_FILE):
                            open(TARGET_FILE, "w+").close()
                        with open(TARGET_FILE, "a") as tf:
                            tf.write(new_line)
                            tf.write("\n")
            flag += 1

# get class name from original txt file


def get_cn():
    with open(SOURCE_FILE, "r") as sf:
        for line in sf:
            if line.startswith("---"):
                # 读取target文件
                with open(TARGET_FILE, "a") as tf:
                    # write 100 '-' into tf
                    tf.write("--"*100)
                    tf.write("\n")
            else:
                first_space = line.find(" ")
                new_line = line[:first_space]
                with open(TARGET_FILE, "a") as tf:
                    tf.write(new_line)
                    tf.write("\n")


def main():
    get_fm()


if __name__ == "__main__":
    main()
