import tkinter as tk
from tkinter import ttk
import zipfile
import os
import threading

# 创建主窗口
root = tk.Tk()
root.title("解压缩进度")

# 设置窗口大小
root.geometry("400x150")

# 创建进度条
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=50)


# 更新进度条的函数
def update_progress_bar(value):
    progress_bar['value'] = value
    root.update_idletasks()


# 解压函数
def unzip_file():
    zip_path = 'cfgzip/cfg.zip'
    extract_path = 'config'

    # 打开压缩文件
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_files = len(zip_ref.infolist())
        for i, file in enumerate(zip_ref.infolist()):
            zip_ref.extract(file, extract_path)
            update_progress_bar((i + 1) / total_files * 100)

    # 关闭窗口
    root.quit()


# 使用线程来解压文件，以免阻塞主线程
threading.Thread(target=unzip_file).start()

# 运行主窗口
root.mainloop()
