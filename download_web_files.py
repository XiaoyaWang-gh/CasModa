import requests
import os
from tqdm import tqdm

urls = [
    # "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/config.json",
    # "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/generation_config.json",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model-00001-of-00007.bin",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model-00002-of-00007.bin",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model-00003-of-00007.bin",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model-00004-of-00007.bin",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model-00005-of-00007.bin",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model-00006-of-00007.bin",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model-00007-of-00007.bin",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/pytorch_model.bin.index.json",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/special_tokens_map.json",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/tokenizer.json",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/tokenizer.model",
    "https://huggingface.co/codellama/CodeLlama-34b-Instruct-hf/resolve/main/tokenizer_config.json"
]

filepath = "codellama/CodeLlama-34b-Instruct-hf"
proxy = "http://127.0.0.1:7890"


def download_file(url, proxy):
    filename = url.split("/")[-1]
    download_path = os.path.join(filepath, filename)

    proxies = {
        "http": proxy,
        "https": proxy
    }

    response = requests.get(url, stream=True, verify=False, proxies=proxies)
    response.raise_for_status()

    file_size = int(response.headers.get("Content-Length", 0))  # 获取待下载的文件大小
    chunk_size = 8192  # 读取的数据块的大小是8千字节

    with open(download_path, "wb") as file, tqdm(
        total=file_size, unit="B", unit_scale=True, unit_divisor=1024, desc=filename
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                file.write(chunk)
                progress_bar.update(1)


for url in urls:
    download_file(url, proxy)
