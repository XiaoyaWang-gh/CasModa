import os
import subprocess

from util.strUtils import make_classpath

# 1f要测试的类：

global_pro_ver = "26f_data"

libpath = r"C:\Libraries\maven-3.5.0\lib\*"

focal_class_path, middle_path, test_class_path, module_path = "", "", "", ""
test_class_list = []


path_tuple_dict = {
    "1f_chart": (
        r"C:\dataset\d4j-spec5\4_chart\1f\source",
        r"org\jfree\chart",
        r"C:\dataset\d4j-spec5\4_chart\1f\tests",
        "org.jfree.chart"
    ),
    "1f_data": (
        r"C:\dataset\d4j-spec5\4_chart\1f\source",
        r"org\jfree\data",
        r"C:\dataset\d4j-spec5\4_chart\1f\tests",
        "org.jfree.data"
    ),
    "26f_chart": (
        r"C:\dataset\d4j-spec5\4_chart\26f\source",
        r"org\jfree\chart",
        r"C:\dataset\d4j-spec5\4_chart\26f\tests",
        "org.jfree.chart"
    ),
    "26f_data": (
        r"C:\dataset\d4j-spec5\4_chart\26f\source",
        r"org\jfree\data",
        r"C:\dataset\d4j-spec5\4_chart\26f\tests",
        "org.jfree.data"
    )
}

focal_class_path, middle_path, test_class_path, module_path = path_tuple_dict.get(
    global_pro_ver)


class_list_dict = {
    "1f_chart": ["CategoryPlotTest", "MinMaxCategoryRendererTest", "MultiplePiePlotTest",
                 "StatisticalBarRendererTest", "XYPlotTest",
                 "AbstractCategoryItemRendererTest", "BorderArrangementTest",  "ValueMarkerTest",
                 "ShapeListTest", "ShapeUtilitiesTest", "StandardToolTipTagFragmentGeneratorTest"],
    "1f_data": ["DatasetUtilitiesTest", "DefaultBoxAndWhiskerCategoryDatasetTest", "DefaultIntervalCategoryDatasetTest",
                "DefaultKeyedValuesTest", "DefaultKeyedValues2DTest", "KeyedObjects2DTest",
                "TimePeriodValuesTest", "TimeSeriesTest", "WeekTest"],
    "26f_chart": ["CategoryPlotTest", "MinMaxCategoryRendererTest", "MultiplePiePlotTest", "StatisticalBarRendererTest", "XYPlotTest",
                  "AxisTest",  "GrayPaintScaleTest", "PiePlotTest"],
    "26f_data": ["KeyedObjects2DTest", "TimeSeriesTest",
                 "XYSeriesTest"]
}

'''
重复类的主版本
'CategoryPlotTest' >> chart
'MinMaxCategoryRendererTest' >> chart
'MultiplePiePlotTest' >> chart
'StatisticalBarRendererTest' >> chart
'XYPlotTest' >> chart
'KeyedObjects2DTest' >> data
'TimeSeriesTest' >> data
'''

test_class_list = class_list_dict.get(global_pro_ver)


def test_compile_command(test_class):
    ab_test_dir = os.path.join(
        test_class_path, middle_path, "generated_by_chatgpt")
    classpath = make_classpath(
        focal_class_path, middle_path, ab_test_dir, libpath)
    compile_command = "javac -encoding ISO-8859-1 -cp " + classpath + \
        ab_test_dir + "\\" + test_class+"1.java"

    compile_result = subprocess.run(compile_command, shell=True,
                                    capture_output=True, text=True)

    if compile_result.returncode == 0:
        print("Compile successfully!")
        return
    print(f"compile_result.stdout :\n{compile_result.stdout}")
    print(f"compile_result.stderr :\n{compile_result.stderr}")
    print(f"execute_command : \n{compile_command}")


def test_execute_command(test_class):
    #
    classpath = make_classpath(focal_class_path, middle_path,
                               test_class_path, middle_path+"\\generated_by_chatgpt", libpath)
    # 决定要不要
    testclass = module_path+".generated_by_chatgpt."+test_class+"1"

    execute_command = "java -cp "+classpath + \
        "org.junit.runner.JUnitCore " + testclass

    execute_result = subprocess.run(execute_command, shell=True,
                                    capture_output=True, text=True)

    if execute_result.returncode == 0:
        print("Execute successfully!")
        return
    print(f"execute_result.stdout :\n{execute_result.stdout}")
    print(f"execute_result.stderr :\n{execute_result.stderr}")
    print(f"execute_command : \n{execute_command}")


def together_test(pro_ver):
    '''
    对特定项目的pro_ver版本中的测试壳子进行统一测试(28,24也太多了一点！！)
    '''
    for i, test_class in enumerate(test_class_list):
        print(f"----------{i}----------")
        test_compile_command(test_class)
        test_execute_command(test_class)


def main():
    together_test(global_pro_ver)


if __name__ == "__main__":
    main()
