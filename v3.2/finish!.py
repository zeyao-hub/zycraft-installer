import tkinter as tk
import webbrowser

def on_closing():
    webbrowser.open("https://mc.lzyablo.top/mods")
    root.destroy()

root = tk.Tk()
root.title("Finish")
root.geometry("200x100")

label = tk.Label(root, text="Finish")
label.pack(pady=20)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
