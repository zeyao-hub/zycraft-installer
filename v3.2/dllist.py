import os
import requests
from bs4 import BeautifulSoup

# 定义本地和远程目录路径
local_mods_dir = 'modszip'
remote_mods_url = 'https://mcmods2333.flyqilai.top/mods/'

# 定义输出文件路径
local_missing_file = 'update/updatelist/local_missing.txt'
remote_missing_file = 'update/updatelist/remote_missing.txt'

# 创建输出目录（如果不存在）
os.makedirs(os.path.dirname(local_missing_file), exist_ok=True)

# 获取本地文件列表
local_files = {f for f in os.listdir(local_mods_dir) if f.endswith('.zip')}

# 获取远程文件列表
response = requests.get(remote_mods_url)
soup = BeautifulSoup(response.text, 'html.parser')
remote_files = {a['href'].replace(remote_mods_url, '') for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')}

# 找出本地缺少的文件
local_missing = remote_files - local_files
with open(local_missing_file, 'w') as f:
    for file in local_missing:
        f.write(file + '\n')

# 找出远程缺少的文件
remote_missing = local_files - remote_files
with open(remote_missing_file, 'w') as f:
    for file in remote_missing:
        f.write(file + '\n')

print("比对完成，结果已保存到 update/updatelist 目录。")
