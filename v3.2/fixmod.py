import os
import requests
from tqdm import tqdm

# 定义文件路径和目标目录
input_file = 'update/updatelist/local_missing.txt'
target_directory = 'modszip'

# 确保目标目录存在
os.makedirs(target_directory, exist_ok=True)

# 读取链接文件
with open(input_file, 'r') as file:
    urls = file.readlines()

# 下载每个文件
for url in tqdm(urls, desc="Downloading files", bar_format="{l_bar}{bar:20}{r_bar}", colour="green"):
    url = url.strip()
    if url:
        # 获取文件名
        file_name = os.path.basename(url)
        file_path = os.path.join(target_directory, file_name)

        # 下载文件
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # 检查请求是否成功

            # 将文件写入目标目录
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

print("All downloads completed.")