'''
prompt_prefix_query.py
'''
import os
from .prompt_father import Prompt
from mytemplate import prefix_template as pt
from dotenv import load_dotenv

load_dotenv()
pro = os.getenv('PROJECT')

instruction_dict = {
    "vanilla": "Generate test input in the following java code:\n",
    "well_crafted": "Your task now is only to construct the test inputs, not the test assertions. Use CLASS_CONSTRUCTOR to get CLASS_NAME, then call TEST_METHOD_NAME. Use java without comments. End your reply with END_OF_DEMO.\n"
}


class PrefixPrompt(Prompt):
    def __init__(self, demonstrations, query):
        self.demonstrations = demonstrations
        self.query = query

    def construct_prompt(self) -> str:


        prefix_prompt = instruction_dict["well_crafted"]
        # traverse the demonstrations and call the embed_demo_template
        for i in range(len(self.demonstrations)):
            prefix_prompt += pt.embed_demo_template_updated(
                self.demonstrations[i])

        # for outter cross project 
        # file = f"C:/codes/CodeX/vlis7_backup/CodeX_back_to_chatgpt/txt_repo/langchain4j-validation/{pro}/SWON/golden_prefix_prompt.txt"
        # with open(file,'r') as f:
        #     prefix_prompt = f.read()
            
        prefix_prompt += pt.embed_query_template_updated(self.query)
        
        # print(f"The final prefix prompt looks like: \n {final_prefix_prompt}")
        return prefix_prompt
