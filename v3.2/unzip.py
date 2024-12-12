import os
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox

class ZipExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zip Extractor with Progress Bar")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Extracting zip files...")
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Extraction", command=self.start_extraction)
        self.start_button.pack(pady=10)

    def start_extraction(self):
        self.start_button.config(state=tk.DISABLED)
        self.root.update_idletasks()
        self.extract_zip_files('modszip', 'mods')
        messagebox.showinfo("Info", "All files extracted successfully!")
        self.start_button.config(state=tk.NORMAL)

    def extract_zip_files(self, source_dir, target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        zip_files = [f for f in os.listdir(source_dir) if f.endswith('.zip')]
        total_files = len(zip_files)
        self.progress['maximum'] = total_files

        for index, item in enumerate(zip_files, 1):
            file_path = os.path.join(source_dir, item)
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
                print(f'{item} 解压成功到 {target_dir}')
            except zipfile.BadZipFile:
                print(f'{item} 不是有效的zip文件')
            except Exception as e:
                print(f'解压 {item} 时出错: {e}')

            self.progress['value'] = index
            self.root.update_idletasks()

if __name__ == '__main__':
    root = tk.Tk()
    app = ZipExtractorApp(root)
    root.mainloop()
