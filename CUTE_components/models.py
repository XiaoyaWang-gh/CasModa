import os
import sys
from enum import Enum
from torch import Tensor

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


class Oracle_datapoint:
    def __init__(self,  test_method: str, focalname_paralist: str, test_name: str, oracle: str):
        self.test_method = test_method
        self.focalname_paralist = focalname_paralist
        self.test_name = test_name
        self.oracle = oracle

    def print(self):
        print("测试方法:", self.test_method)
        print("被测方法签名:", self.focalname_paralist)
        print("测试用例名字:", self.test_name)
        print("测试oracle:", self.oracle)

    def toString(self):
        return f"""测试方法: {self.test_method} 
        被测方法签名: {self.focalname_paralist} 
        测试用例名字: {self.test_name} 
        测试oracle: {self.oracle} """


class Prefix_datapoint:
    def __init__(self, constructor: str, test_input: str, classname: str, focalname_paralist: str, testname: str):
        self.constructor = constructor
        self.test_input = test_input
        self.classname = classname  # for exclude self
        self.focalname_paralist = focalname_paralist  # for exclude self, too
        self.testname = testname

    def print(self):
        print("被测类: ", self.classname)
        print("类构造器: ", self.constructor)
        print("被测方法签名: ", self.focalname_paralist)
        print("测试用例名字: ", self.testname)
        print("测试prefix: ", self.test_input)

    def toString(self):
        return f"""被测类:  {self.classname} 
        类构造器: {self.constructor} 
        被测方法签名: {self.focalname_paralist} 
        测试用例名字: {self.testname} 
        测试prefix: {self.test_input} """


class Testcase_datapoint:
    def __init__(self, classname: str, constructor: str, focalname_paralist: str, focal_func:str, test_name: str, test_body: str, unix_tensor: Tensor):
        self.classname = classname
        self.constructor = constructor
        self.focalname_paralist = focalname_paralist
        self.focal_func = focal_func
        self.test_name = test_name
        self.test_body = test_body
        self.unix_tensor = unix_tensor


class Ecommerce_query_jsonpoint:
    def __init__(self, simple_json: str, rich_json: str):
        self.simple_json = simple_json
        self.rich_json = rich_json


class Failed_To_Be_Repair_datapoint:
    def __init__(self, classname: str, focalname_paralist: str, failed_stderr: str, test_unit: str):
        self.classname = classname
        self.focalname_paralist = focalname_paralist
        self.failed_stderr = failed_stderr  # 对于测试失败是stdout
        self.test_unit = test_unit

    def print(self):
        print("classname: ", self.classname)
        print("focalname_paralist: ", self.focalname_paralist)
        print("compile_failed_stderr: ", self.failed_stderr)
        print("test_unit: ", self.test_unit)

    def toString(self):
        return f"""classname: {self.classname}
        focalname_paralist: {self.focalname_paralist}
        compile_failed_stderr: {self.failed_stderr}
        test_unit: {self.test_unit}"""


class Test_Unit_Status(Enum):
    NONE_STATUS = "none_status"
    NOT_COMPILE_SUCCESS = "compile_failed"
    COMPILE_SUCCESS_BUT_NOT_EXECUTE = "compile_success_but_execute_failed"
    EXECUTE_SUCCESS = "execute_success"


class Result_datapoint:
    def __init__(self, id: int, test_unit_compile_time: int, test_unit_execute_time: int, test_unit_status: Test_Unit_Status, passed_test_unit: str = "", compile_suc_execute_fail_unit: str = ""):
        self.id = id
        self.test_unit_compile_time = test_unit_compile_time
        self.test_unit_execute_time = test_unit_execute_time
        self.test_unit_status = test_unit_status

    def toString(self):
        res_str = str(self.id)+", "+str(self.test_unit_compile_time)+", "+str(
            self.test_unit_execute_time)+", "+self.test_unit_status.value+"\n"
        return res_str
