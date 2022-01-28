from tkinterweb import HtmlFrame
import tkinter as tk
import sys

root = tk.Tk()
root.geometry("1000x1000")

htmlGroup = tk.Frame(root, width="500", height="500")
htmlFrame = HtmlFrame(htmlGroup)

htmlFrame.load_website("http://tkhtml.tcl.tk/tkhtml.html")
# htmlFrame.load_html("C:/Users/leite/Desktop/Repos/TKPythonSandbox/output.html")

htmlFrame.pack(fill="both", expand=True)
htmlGroup.pack(side=tk.LEFT)
root.mainloop()