from CUTE_components.models import Prefix_datapoint, Oracle_datapoint, Testcase_datapoint
from typing import List
import os
import torch


class Prefix_Dataset:
    
    def __init__(self, data_path_prefix, constructor_file, test_input_file, classname_file, focalname_paralist_file, testname_file):
        with open(os.path.join(data_path_prefix, constructor_file), "r", encoding="utf-8") as f:
            self.c_list = f.readlines()
        with open(os.path.join(data_path_prefix, test_input_file), "r", encoding="utf-8") as f:
            self.t_list = f.readlines()
        with open(os.path.join(data_path_prefix, classname_file), "r", encoding="utf-8") as f:
            self.cn_list = f.readlines()
        with open(os.path.join(data_path_prefix, focalname_paralist_file), "r", encoding="utf-8") as f:
            self.fnp_list = f.readlines()
        with open(os.path.join(data_path_prefix, testname_file), "r", encoding="utf-8") as f:
            self.tn_list = f.readlines()

    def parse(self, query_id=None) -> List[Prefix_datapoint]:
        assert len(self.c_list) == len(self.t_list) == len( self.cn_list) == len(self.fnp_list) == len(self.tn_list)
        result = []
        cnt = 0
        j = 0
        for i in range(len(self.c_list)):
            if self.c_list[i].strip().startswith("-----"):
                continue
            constructor = self.c_list[i].strip()
            test_input = self.t_list[i].strip()
            classname = self.cn_list[i].strip()
            focalname_paralist = self.fnp_list[i].strip()
            testname = self.tn_list[i].strip()
            j = j+1
            if query_id != None and classname+focalname_paralist == query_id:
                cnt += 1
                continue
            dp = Prefix_datapoint(
                constructor, test_input, classname, focalname_paralist, testname)
            result.append(dp)
        print(f"一共回避了{cnt}条被测方法相同的demo")
        return result


class Oracle_Dataset:
    def __init__(self, data_path_prefix, tm_file, fmn_file, tmn_file, oracle_file):

        # tm_file是由上一阶段生成的test input转化得到的，行数和其他文件不一样，且有分隔符
        with open(os.path.join(data_path_prefix, tm_file), "r", encoding="utf-8") as f:
            self.tm_list = f.readlines()
        with open(os.path.join(data_path_prefix, fmn_file), "r", encoding="utf-8") as f:
            self.fmn_list = f.readlines()
        with open(os.path.join(data_path_prefix, tmn_file), "r", encoding="utf-8") as f:
            self.tmn_list = f.readlines()
        with open(os.path.join(data_path_prefix, oracle_file), "r", encoding="utf-8") as f:
            self.oracle_list = f.readlines()

    def get_tm_nested_list(self, tm_list: list):
        nested_tm_list = []  # list[list[str]]
        inner_list = []
        for tm in tm_list:
            tm = tm.strip()
            if tm.startswith("##ABOVE"):
                nested_tm_list.append(inner_list)
                inner_list = []
            else:
                inner_list.append(tm)
        return nested_tm_list

    def demopool_parse(self) -> List[Oracle_datapoint]:
        # delete the lines starting with ----
        self.fmn_list = [
            line for line in self.fmn_list if not line.startswith("-----")]
        self.tmn_list = [
            line for line in self.tmn_list if not line.startswith("-----")]
        self.oracle_list = [
            line for line in self.oracle_list if not line.startswith("-----")]
        self.tm_list = [
            line for line in self.tm_list if not line.startswith("-----")]
        assert len(self.fmn_list) == len(self.tmn_list) == len(
            self.oracle_list) == len(self.tm_list)

        result = []
        for i in range(len(self.fmn_list)):
            tm = self.tm_list[i].strip()
            fmn = self.fmn_list[i].strip()
            tmn = self.tmn_list[i].strip()
            oracle = self.oracle_list[i].strip()
            result.append(Oracle_datapoint(tm, fmn, tmn, oracle))
        return result


class Testcase_Dataset:
    def __init__(self, data_path_prefix, cn_file, cc_file, fn_file, tn_file, tb_file, ut_file):
        with open(data_path_prefix+"/"+cn_file, "r", encoding="utf-8", errors='ignore') as f:
            self.cn_list = f.readlines()
        with open(data_path_prefix+"/"+cc_file, "r", encoding="utf-8", errors='ignore') as f:
            self.cc_list = f.readlines()
        with open(data_path_prefix+"/"+fn_file, "r", encoding="utf-8", errors='ignore') as f:
            self.fn_list = f.readlines()
        with open(data_path_prefix+"/"+tn_file, "r", encoding="utf-8", errors='ignore') as f:
            self.tn_list = f.readlines()
        with open(data_path_prefix+"/"+tb_file, "r", encoding="utf-8", errors='ignore') as f:
            self.tb_list = f.readlines()
        with open(data_path_prefix+"/"+ut_file, "r", encoding="utf-8", errors='ignore') as f:
            self.ut_list = f.readlines()

    def parse(self, query_id=None) -> List[Testcase_datapoint]:
        self.cn_list = [
            line for line in self.cn_list if not line.startswith("-----")]
        self.cc_list = [
            line for line in self.cc_list if not line.startswith("-----")]
        self.fn_list = [
            line for line in self.fn_list if not line.startswith("-----")]
        self.tn_list = [
            line for line in self.tn_list if not line.startswith("-----")]
        self.tb_list = [
            line for line in self.tb_list if not line.startswith("-----")]
        processed_ut_list = []
        for line in self.ut_list:
            line = line.strip()
            line = line[1:-1]
            num_list = line.split(",")
            value_list = [float(num) for num in num_list]
            # 转化为tensor
            tensor = torch.tensor(value_list).view(1, 768)
            processed_ut_list.append(tensor)

        if len(self.tb_list) == 0:
            assert len(self.cn_list) == len(self.cc_list) == len(
                self.fn_list) == len(self.tn_list) # == len(processed_ut_list)
        else:
            assert len(self.cn_list) == len(self.cc_list) == len(
                self.fn_list) == len(self.tn_list) == len(self.tb_list) # == len(processed_ut_list)

        result = []
        cnt = 0
        for i in range(len(self.cn_list)):
            cn = self.cn_list[i].strip()
            cc = self.cc_list[i].strip()
            fn = self.fn_list[i].strip()
            tn = self.tn_list[i].strip()
            
            if len(processed_ut_list) == 0:
                ut = ""
            else:
                ut = processed_ut_list[i]

            if len(self.tb_list) == 0:
                tb = ""
            else:
                tb = self.tb_list[i].strip()

            if query_id is not None and query_id == cn+fn:
                cnt += 1
                continue
            result.append(Testcase_datapoint(
                cn, cc, fn, tn, tb, ut))
        print(f"一共回避了{cnt}条与被测方法相同的demo")
        return result
