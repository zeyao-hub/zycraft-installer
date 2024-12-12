import tkinter as tk
from tkinter import messagebox
import subprocess

def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
        messagebox.showinfo("success!", f"{script_name} Successfully run")
    except subprocess.CalledProcessError:
        messagebox.showerror("error", f"run {script_name} Error")

def create_gui():
    root = tk.Tk()
    root.title("other")
    root.geometry("200x290")

    label = tk.Label(root, text="other", font=("Arial", 14))
    label.pack(pady=20)

    button1 = tk.Button(root, text="updatemods", command=lambda: run_script("1.py"), font=("Arial", 12))
    button1.pack(pady=10)

    button2 = tk.Button(root, text="updateshaderpacks", command=lambda: run_script("shaderpacks.py"), font=("Arial", 12))
    button2.pack(pady=10)

    button3 = tk.Button(root, text="installJava", command=lambda: run_script("javaurl.py"), font=("Arial", 12))
    button3.pack(pady=10)

    button4 = tk.Button(root, text="Update module dependency files", command=lambda: run_script("mod_resourcepkg.py"), font=("Arial", 12))
    button4.pack(pady=10)


    button5 = tk.Button(root, text="update_resourcepkg", command=lambda: run_script("resourcepkg.py"), font=("Arial", 12))
    button5.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
