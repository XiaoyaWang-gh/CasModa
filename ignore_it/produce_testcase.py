# 目的：用于将消融实验生成的test body包裹成test case
SF1 = "C:/codes/CodeX/CodeX/txt_repo/ablation/testcase/gson/output/testbody_byRandomOrderDemos.txt"
SF2 = "C:/codes/CodeX/CodeX/txt_repo/ablation/testcase/gson/query_set/testname.txt"
TF = "C:/codes/CodeX/CodeX/txt_repo/ablation/testcase/gson/output/testcase_byRandomOrderDemos.txt"

with open(SF1, "r") as f1, open(SF2, "r") as f2, open(TF, "a") as f3:
    tbList = f1.readlines()
    tnList = f2.readlines()
    assert len(tbList) == 2*len(tnList)
    for i in range(len(tnList)):
        tb = tbList[2*i]
        tn = tnList[i]
        f3.write("@Test public void _" + tn.strip() +
                 " { " + tb.strip() + " }\n")
