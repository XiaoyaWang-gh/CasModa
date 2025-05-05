from .prompt_father import Prompt
from mytemplate import testcase_template as tt

instruction_dict = {
    "vanilla": "generate test case in the following java code:\n",
    "updated": "Your task is to generate a test case. Firstly, use CLASS_CONSTRUCTOR to get CLASS_NAME, then call TEST_METHOD_NAME. Secondly, generate a test assertion to replace the <OraclePlaceHolder> in UNIT_TEST. Only variables that appear in UNIT_TEST can be used. Use java without comments.",
    "250503-ver":"250503-ver-en.txt"
}


class TestcasePrompt(Prompt):
    def __init__(self, demonstrations, query):
        self.demonstrations = demonstrations
        self.query = query

    def construct_prompt(self) -> str:
        final_testcase_prompt = instruction_dict["updated"]
        # traverse the demonstrations and call the embed_demo_template
        for i in range(len(self.demonstrations)):
            final_testcase_prompt += tt.embed_demo_template(
                self.demonstrations[i])
        final_testcase_prompt += tt.embed_query_template(self.query)

        # print(f"The final prefix prompt looks like: \n {final_prefix_prompt}")
        return final_testcase_prompt

    def construct_ecommerce_prompt(self) -> str:
        instruction_file = instruction_dict["250503-ver"]
        with open(instruction_file, "r") as f:
            ecommerce_instruction = f.read()
        final_testcase_prompt = ecommerce_instruction
        for i in range(len(self.demonstrations)):
            final_testcase_prompt += tt.embed_ecommerce_demo_template(
                self.demonstrations[i])
        final_testcase_prompt += tt.embed_ecommerce_query_template(self.query)

