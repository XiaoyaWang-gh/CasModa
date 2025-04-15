'''
本文件的目的是：去重，这样既能省调用次数，又能省最后核实时候的人力成本
杜绝有完全相同的测试输入
只在最后统计时"复重(chong)"
'''

pname = "chart1"

DIR_PATH = f"C:/codes/CodeX/CodeX/txt_repo/prefix/query_set/{pname}/before_deduplicate/"
SF2 = "focal_method.java"
TF1 = "xyplot_fm.java"
TF2 = "xyplot_cnt.java"


def main():

    fm_file = open(DIR_PATH+SF2, "r")
    xyplot_fm = open(DIR_PATH+TF1, "a")
    xyplot_cnt = open(DIR_PATH+TF2, "a")
    try:
        # read cn_file as list
        fm_list = fm_file.readlines()
        # 926 - 1309
        xyplot_origin_list = fm_list[925:1309]
        xyplot_dedu_list = list(set(xyplot_origin_list))
        cnt = 0
        for line in xyplot_dedu_list:
            xyplot_fm.write(line)
            xyplot_cnt.write(str(xyplot_origin_list.count(line))+"\n")
            cnt += xyplot_origin_list.count(line)
        assert cnt == len(xyplot_origin_list)
    finally:
        fm_file.close()
        xyplot_fm.close()
        xyplot_cnt.close()


if __name__ == '__main__':
    main()
