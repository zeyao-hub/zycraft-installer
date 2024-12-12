import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText


def run_script(script_name):
    process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def update_output(process, text_widget):
    while True:
        output = process.stdout.readline()
        if process.poll() is not None and output == b'':
            break
        if output:
            text_widget.insert(tk.END, output.decode('utf-8'))
            text_widget.see(tk.END)
    process.stdout.close()


def run_all_scripts():
    scripts = ['clear.py', 'dllist.py', 'delup_date.py', 'missurl.py', 'fixmod.py', 'unzip.py']
    for script in scripts:
        process = run_script(script)
        update_output(process, text_widget)

    messagebox.showinfo("complete!", "Finish")


# 创建主窗口
root = tk.Tk()
root.title("请等待Finish窗口弹出！...")

# 创建滚动文本框来显示输出
text_widget = ScrolledText(root, wrap=tk.WORD, width=100, height=30)
text_widget.pack(padx=10, pady=10)

# 运行脚本并显示输出
root.after(100, run_all_scripts)

# 启动 Tkinter 主循环
root.mainloop()
