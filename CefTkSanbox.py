from cefpython3 import cefpython as cef
import platform
import sys
import tkinter as tk

def main(root):

    root.geometry("600x600")
    label = tk.Label(root, text="Press Enter to browse Internet", fg="blue", font="Arial 20")
    label.pack()
    userInput = tk.StringVar()
    entry = tk.Entry(root, textvariable=userInput, font="Arial 14")
    entry.pack()
    userInput.set("C:\\Users\\leite\\Desktop\\Repos\\TKPythonSandbox\\output.html")
    entry.focus()
    entry.bind("<Return>", lambda x: open_link(entry.get()))

    root.mainloop()
    cef.Shutdown()

def open_link(url):
    print(url)
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    cef.CreateBrowserSync(url=url, window_title=url)
    cef.MessageLoop()
    main()

if __name__ == '__main__':
    global root
    root = tk.Tk()
    main(root)
