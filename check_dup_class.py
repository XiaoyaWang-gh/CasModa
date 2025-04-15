# 该文件的作用是检测是否在高铁上做得两个testClass_place.json，是否涵盖了正确的id
import os

class_list_dict = {
    "1f_chart": ["AbstractCategoryItemRendererTest", "BorderArrangementTest", "CategoryPlotTest", "MinMaxCategoryRendererTest",
                 "MultiplePiePlotTest", "ShapeListTest", "ShapeUtilitiesTest", "StandardToolTipTagFragmentGeneratorTest",
                 "StatisticalBarRendererTest", "ValueMarkerTest", "XYPlotTest"],
    "1f_data": ["DatasetUtilitiesTest", "DefaultBoxAndWhiskerCategoryDatasetTest", "DefaultIntervalCategoryDatasetTest",
                "DefaultKeyedValuesTest", "DefaultKeyedValues2DTest", "KeyedObjects2DTest",
                "TimePeriodValuesTest", "TimeSeriesTest", "WeekTest"],
    "26f_chart": ["AxisTest", "CategoryPlotTest", "GrayPaintScaleTest", "MinMaxCategoryRendererTest",
                  "MultiplePiePlotTest", "PiePlotTest", "StatisticalBarRendererTest", "XYPlotTest"],
    "26f_data": ["KeyedObjects2DTest", "TimeSeriesTest", "XYSeriesTest"]
}


def duplicate_elements(_class_list_dict):
    '''
    一共24个类，现在所有版本加起来有31个，说明有7个既在1f，又在26f，这个方法的作用是将这7个类找出来
    这样在主版本做好壳子以后，可以直接粘贴进副版本
    '''
    _1f_list = []
    _26f_list = []
    for key in _class_list_dict:
        if key.startswith("1f"):
            _1f_list = _1f_list + _class_list_dict.get(key)
        elif key.startswith("26f"):
            _26f_list = _26f_list + _class_list_dict.get(key)

    print(f"len of _1f_list : {len(_1f_list)}")
    print(f"len of _26f_list : {len(_26f_list)}")

    dup_list = []
    for element in _1f_list:
        if element in _26f_list:
            dup_list.append(element)

    print(f"7个重复类 : {dup_list}")


def main():
    duplicate_elements(class_list_dict)


if __name__ == "__main__":
    main()
