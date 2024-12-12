import os
import requests
import tkinter as tk
from tkinter import ttk
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# Function to download a file and update the progress bar
def download_file(url, save_path, progress, total_size):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        downloaded_size = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                progress.set(downloaded_size / total_size * 100)
                root.update_idletasks()


# Function to get all zip file URLs from the given webpage
def get_zip_file_urls(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    zip_urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.zip'):
            zip_urls.append(urljoin(base_url, href))
    return zip_urls


# Main function to download all zip files
def download_all_files():
    base_url = 'https://mcmods2333.flyqilai.top/mod_resourcepkg/pointblank/'
    save_dir = 'pointblank'
    os.makedirs(save_dir, exist_ok=True)

    zip_urls = get_zip_file_urls(base_url)
    total_files = len(zip_urls)
    progress_bar['maximum'] = 100 * total_files

    for i, zip_url in enumerate(zip_urls):
        filename = os.path.join(save_dir, os.path.basename(zip_url))
        response = requests.head(zip_url)
        total_size = int(response.headers.get('content-length', 0))
        progress.set(0)

        download_file(zip_url, filename, progress, total_size)
        progress_bar['value'] += 100
        root.update_idletasks()

    root.quit()


# Setup GUI
root = tk.Tk()
root.title("Download Progress")

progress = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress, maximum=100)
progress_bar.pack(padx=10, pady=10, fill=tk.X)

root.after(100, download_all_files)  # Start downloading after 100ms

root.mainloop()
