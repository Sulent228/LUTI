# LUT Interface 2025, version - 0.0.0-alpha (Initial version) by @offjjo

from tkinter import *; from tkinter import messagebox; from pathlib import Path; import os; import shutil; import Explorer; import Editor

def MainRoot():
    root = Tk()
    root.title("LUT Interface 2025 by @offjjo")
    root.geometry("500x500")
    
    MainFrame = Frame(root)
    MainFrame.pack(fill=BOTH, expand=True)
    
    ExplorerButton = Button(MainFrame, text="Explorer", command=Explorer.Init)
    ExplorerButton.pack()
    
    EditorButton = Button(MainFrame, text="File Editor", command=Editor.Init)
    EditorButton.pack()
    
    root.protocol("WM_DELETE_WINDOW", lambda:on_closing(root))
    
    root.mainloop()
    
def on_closing(root):
    # Здесь вы можете добавить логику, которая выполняется перед закрытием
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()  # Закрывает окно

def LUTIInit():
    MainRoot()

if __name__ == "__main__":
    LUTIInit()