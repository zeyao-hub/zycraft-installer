import os
import requests
from tqdm import tqdm
from urllib.parse import urljoin, urlparse

# 设置下载的URL和本地目录
base_url = 'https://mcmods2333.flyqilai.top/resourcepkg/resourcepacks/'
save_dir = './resourcepacks'

# 确保本地目录存在
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024  # 1 KB

    with open(save_path, 'wb') as file, tqdm(
        desc=save_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=chunk_size):
            bar.update(len(data))
            file.write(data)

def find_and_download_files(base_url, save_dir):
    response = requests.get(base_url)
    links = [line.split('"')[1] for line in response.text.splitlines() if 'href="' in line]

    for link in links:
        if link.endswith('/'):  # 如果是目录则递归下载
            subdir_url = urljoin(base_url, link)
            subdir_path = os.path.join(save_dir, link)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path)
            find_and_download_files(subdir_url, subdir_path)
        else:  # 如果是文件则下载
            file_url = urljoin(base_url, link)
            file_path = os.path.join(save_dir, link.split('/')[-1])
            print(f'Downloading {file_url} to {file_path}')
            download_file(file_url, file_path)

# 执行下载
find_and_download_files(base_url, save_dir)
