'''
此文件的目的是将demo pool 中的test method中的oraclePlaceHolder换成oracle 
再得到方法体，用于完整检索的消融实验
'''

SF1 = "C:/codes/CodeX/CodeX/txt_repo/mixed/gson/8_tm.txt"
SF2 = "C:/codes/CodeX/CodeX/txt_repo/mixed/gson/7_ora.txt"
TF1 = "C:/codes/CodeX/CodeX/txt_repo/mixed/gson/9_tb.txt"

PLACE_HOLDER = "\"<OraclePlaceHolder>\";"

with open(SF1, "r") as tmFile:
    tmList = tmFile.readlines()

with open(SF2, "r") as oraFile:
    oraList = oraFile.readlines()

with open(TF1, "a") as tbFile:
    assert len(tmList) == len(oraList)
    for i in range(len(tmList)):
        # judge if there is only one "<OraclePlaceHolder>"; in tm
        tm = tmList[i].strip()
        if tm.count(PLACE_HOLDER) == 1:
            ora = oraList[i].strip()
        # if so, replace
            tmp = tm.replace(PLACE_HOLDER, ora)
        # then delete testName and {}
            leftPos = tmp.find('{')
            # print(leftPos)
            assert isinstance(leftPos+1, int) == True
            assert len(tmp) > leftPos+1
            tb = tmp[leftPos+1:-1]
            # tb = tmp[:-1]
            tbFile.write(tb+"\n")
        # if not, write white line, and output the order
        else:
            print(f"第{i+1}条是需要手动替换的")
            tbFile.write("\n")
