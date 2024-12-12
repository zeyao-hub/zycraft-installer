import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.update_download_button = tk.Button(self)
        self.update_download_button["text"] = "Download_all"
        self.update_download_button["command"] = self.run_update_or_download
        self.update_download_button.pack(side="top")

        self.fix_button = tk.Button(self)
        self.fix_button["text"] = "other"
        self.fix_button["command"] = self.run_fix
        self.fix_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.output_monitor = ScrolledText(self, wrap='word', height=20, width=80)
        self.output_monitor.pack(side="bottom")

    def run_script(self, script_name):
        process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            self.output_monitor.insert(tk.END, line)
            self.output_monitor.see(tk.END)
        process.stdout.close()
        process.wait()

    def run_update_or_download(self):
        self.output_monitor.delete(1.0, tk.END)
        threading.Thread(target=self.run_all_scripts).start()

    def run_fix(self):
        self.output_monitor.delete(1.0, tk.END)
        threading.Thread(target=self.run_script, args=('other.py',)).start()

    def run_all_scripts(self):
        scripts = [
            'clear.py',
            'shaderpacks.py',
            'resourcepkg.py',
            'dllist.py',
            'delup_date.py',
            'missurl.py',
            'fixmod.py',
            'mod_resourcepkg.py',
            'cfg.py',
            'unzipcfg.py',
            'unzip.py',
            'finish!.py',
        ]
        for script in scripts:
            self.run_script(script)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
