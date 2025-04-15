'''
本文件的目的是从完整的被测方法得到被测方法签名
'''
pname = "chart1"

SOURCE_FILE = f"C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/{pname}/xyplot_fm.java"
TARGET_FILE = f"C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/{pname}/xyplot_focalname_paralist.java"


def main():
    with open(SOURCE_FILE, "r") as sf:
        for line in sf:
            line = line.strip()
            if line.startswith("-----"):
                with open(TARGET_FILE, "a") as tf:
                    tf.write(line)
                    tf.write("\n")
            else:
                m = line.strip()
                m_list = m.split(" ")
                with open(TARGET_FILE, "a") as tf:
                    if '(' in m_list[2]:
                        posL = m.find(m_list[2])
                        tmp = m[posL:]
                        posR = tmp.find(')')
                        tf.write(tmp[:posR+1])
                        tf.write("\n")
                    else:  # 说明遇到static了！
                        posL = m.find(m_list[3])
                        tmp = m[posL:]
                        posR = tmp.find(')')
                        tf.write(tmp[:posR+1])
                        tf.write("\n")


if __name__ == "__main__":
    main()
