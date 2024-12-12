import os
import webbrowser

def open_java_website():
    if os.name == 'nt':  # Windows
        url = 'https://www.java.com/zh-CN/'
    else:  # Linux or other platforms
        url = 'https://flyqilai.top/java'

    webbrowser.open(url)

if __name__ == "__main__":
    open_java_website()
