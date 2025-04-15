'''
prompt_oracle_query
'''
import os
from .prompt_father import Prompt
from mytemplate import oracle_template as ot
from dotenv import load_dotenv

load_dotenv()
pro = os.getenv('PROJECT')

instruction_dict = {
    "vanilla": "Generate oracle in the following java code:\n",
    "well_crafted": "Your task now is to generate a test assertion to replace the <OraclePlaceHolder> in UNIT_TEST. Only variables that occur after the last UNIT_TEST can be used. Use java without comments. End your reply with END_OF_DEMO.\n"
}


class OraclePrompt(Prompt):
    def __init__(self, demonstrations, query):
        self.demonstrations = demonstrations
        self.query = query

    def construct_prompt(self) -> str:
        oracle_prompt = instruction_dict["well_crafted"]
        # traverse the demonstrations and call the embed_demo_template
        for i in range(len(self.demonstrations)):
            oracle_prompt += ot.embed_demo_template(
                self.demonstrations[i])
        
        # for outter cross project 
        # file = f"C:/codes/CodeX/vlis7_backup/CodeX_back_to_chatgpt/txt_repo/langchain4j-validation/{pro}/SWON/golden_oracle_prompt.txt"
        # with open(file,'r') as f:
        #     oracle_prompt = f.read()
        oracle_prompt += ot.embed_query_template(self.query)

        # print(f"The final oracle prompt looks like: \n {final_oracle_prompt}")
        return oracle_prompt
