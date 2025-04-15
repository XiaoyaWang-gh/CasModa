# April 3 created for ablation study
# test_body.txt 这个文件是之前没有的，需要将test_method.txt转化成它，于是写了produce_test_body.py

SF = "txt_repo/mixed/gson/8_tm.txt"
TF = "txt_repo/ablation/testcase/gson/demo_pool/test_body.txt"


# 读入方法，返回方法体
def undress_test_method(method: str) -> str:
    # 得到第一个{的位置
    start = method.find("{")
    return method[start + 1:-1]


def main():
    with open(SF, "r", encoding="utf-8") as sf, open(TF, "a", encoding="utf-8") as tf:
        for line in sf:
            tf.write(undress_test_method(line)+'\n')


if __name__ == "__main__":
    main()
