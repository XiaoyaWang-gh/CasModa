# 这个文件是将test_method中的<OralcePlaceHolder>替换为stage2生成的oracle
# 如果生成的Oralce中含有assert，那么替换前置PlaceHolder，否则替换后置

pname = "cli"
query_num_dict = {"gson": 129, "cli": 255,
                  "csv": 202, "chart": 989, "lang": 1215}

shot_type = "shot_5"
order_type = "reverse"

# 两种选择 !!! 这个文件要改
TEST_METHOD_FILE_WITH_PLACEHOLDER = f"txt_repo/gpt_output/{pname}/2_transition_stage/{shot_type}/{order_type}/CUTE_testMethod.txt"
# 第二阶段生成结果
ORACLE_GENERATED_FILE = f"txt_repo/gpt_output/{pname}/3_oracle_stage/{shot_type}/{order_type}/CUTE_oracle.txt"

TEST_UNIT_FILE = f"txt_repo/gpt_output/{pname}/4_final_stage/{shot_type}/{order_type}/CUTE_testCase.txt"

PLACE_HOLDER = '''"<OraclePlaceHolder>";'''
win10_path_prefix = "C:/codes/CodeX/vlis7_backup/CodeX_back_to_chatgpt/"


def wipeout_oracle_placeholder(oracle: str, testMethod: str) -> str:
    # find "<OraclePlaceHolder>"; and replace it with oracle
    testUnit = testMethod.replace(PLACE_HOLDER, oracle)
    return testUnit


def get_test_unit():
    with open(win10_path_prefix+TEST_METHOD_FILE_WITH_PLACEHOLDER, "r") as test_method_file:
        testMethodList = test_method_file.readlines()
        testMethodList = [
            line for line in testMethodList if not line.startswith("  ##ABOVE")]
    assert len(testMethodList) == query_num_dict[pname]

    with open(win10_path_prefix+ORACLE_GENERATED_FILE, "r") as oracle_file:
        oracle_list = []
        content = oracle_file.read()
        split_content = content.split("##ABOVE")
        for oracle in split_content:
            oracle = oracle.strip()
            if oracle:
                index = oracle.find("-----------------")
                if index != -1:
                    oracle = oracle[index+150:]
                oracle = oracle.replace('\n', '')  # multi-line to single
                oracle_list.append(oracle)
        oracle_list = oracle_list[:-1]
    assert len(oracle_list) == len(testMethodList)

    # 在找到oracle和test method without oracle的对应关系后，调用wipeout_oracle_placeholder()
    test_unit_file = open(win10_path_prefix+TEST_UNIT_FILE, "a")

    # 对于csv来说，生成的oracle中都含有assert，不再考虑前置后置的事情
    for i in range(len(oracle_list)):
        oracle = oracle_list[i]
        test_unit_file.write(
            wipeout_oracle_placeholder(oracle, testMethodList[i]))

    return


def main():
    get_test_unit()


if __name__ == "__main__":
    main()
