# 构造测试类的名称

vlis7_path_prefix = "/data2/chaoni/xiaoyawang/CodeX/"
DIR_PATH = "txt_repo/prefix/query_set/lang/"
SOURCE_FILE = "focalname_paralist.txt"
TARGET_FILE = "testname.txt"


def main():
    with open(vlis7_path_prefix+DIR_PATH+SOURCE_FILE, "r", encoding="utf-8") as sf:
        with open(vlis7_path_prefix+DIR_PATH+TARGET_FILE, "w", encoding="utf-8") as tf:
            for line in sf:
                line = line.strip()
                if line.startswith("-------"):
                    tf.write(line)
                    tf.write("\n")
                else:
                    pos_left = line.find("(")
                    focalname = line[:pos_left]
                    testname = "test" + \
                        focalname[0].upper() + focalname[1:] + "()"
                    tf.write(testname)
                    tf.write("\n")


if __name__ == "__main__":
    main()
