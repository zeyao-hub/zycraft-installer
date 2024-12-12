import tkinter as tk
from tkinter import ttk
import requests
from threading import Thread
import os

def download_file(url, dest_folder):
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        total_length = int(r.headers.get('content-length', 0))
        with open(local_filename, 'wb') as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress.set(downloaded / total_length * 100)
                    progress_bar.update()
    root.quit()

def start_download():
    url = 'https://mcmods2333.flyqilai.top/gameconfig/config/cfg.zip'
    dest_folder = 'cfgzip'
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    Thread(target=download_file, args=(url, dest_folder)).start()

# GUI Setup
root = tk.Tk()
root.title('File Downloader')

progress = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress, maximum=100)
progress_bar.pack(padx=10, pady=10, fill='x')

start_download()

root.mainloop()
