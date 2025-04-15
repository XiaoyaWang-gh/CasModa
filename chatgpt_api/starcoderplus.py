import os
import sys
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3' 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

vlis7_path_prefix = "/data2/chaoni/xiaoyawang/CodeX/"
checkpoint = "/data2/chaoni/xiaoyawang/LLM_ckpts/starcodeplus"
STOP_STR = "END"

my_token_num = int(sys.argv[2])

class StarCoderPlusModel:
    def __init__(self, output_file):
        self.output_file = output_file
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint,device_map='auto',load_in_8bit=True)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        

    def generate(self, input_prompt):
        self.pipe = pipeline("text-generation", repetition_penalty=1.2,model=self.model, tokenizer=self.tokenizer, max_new_tokens=len(input_prompt)*0.2+my_token_num,stop_sequence=STOP_STR)
        # 切片的目的：(1)删去开头的input_prompt，(2)删去结尾的STOP_STR
        result = self.pipe(input_prompt)[0]["generated_text"][len(input_prompt):-4].replace("\n", " ")
        print(result)
        with open(vlis7_path_prefix+self.output_file, "a") as tf:
            tf.write(result)