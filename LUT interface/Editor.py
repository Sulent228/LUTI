from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import *
from tkinter.messagebox import *
import os
import threading

# Global Variables
SelectedFile = None
root = None
AboutRoot = None
RootName = os.path.basename(__file__)

# File Menu Functions
def File_Menu_New(TextBox):
    global SelectedFile
    TextBox.delete("1.0", END)
    SelectedFile = None
    root.title(RootName)

def File_Menu_Save(TextBox):
    try:
        global SelectedFile
        with open(SelectedFile, "w+", encoding="utf-8") as File:
            File.write(TextBox.get("1.0", END))
            root.title(RootName + f' "{os.path.basename(SelectedFile)}"')
            return File
    except:
        showerror("Error", "Файл не найден.")

def File_Menu_SaveAs(TextBox):
    global SelectedFile
    try:
        GetFile = asksaveasfilename(title="Выбор файла",
                                     confirmoverwrite=True,
                                     defaultextension="txt",
                                     initialfile="PythonFile.py")
        
        with open(GetFile, "w+", encoding="utf-8") as File:
            File.write(TextBox.get("1.0", END))
            SelectedFile = File.name
        root.title(RootName + f' "{os.path.basename(SelectedFile)}"')
        return GetFile
    except:
        pass

def File_Menu_Open(TextBox):
    global SelectedFile
    try:
        OpenFile = askopenfilename()
        TextBox.delete("1.0", END)
        with open(OpenFile, "r", encoding="utf-8") as File:
            TextBox.insert("0.1", File.read())
        SelectedFile = OpenFile
        root.title(RootName + f' "{os.path.basename(SelectedFile)}"')
    except:
        pass

def File_Init(TextBox, run_button):
    if len(TextBox.get("0.1", END)) == 0 or TextBox.get("0.1", END).isspace():
        return

    global SelectedFile
    if SelectedFile is None or not os.path.exists(SelectedFile):
        result = askyesno(title="Подтверждение операции", message="Для запуска кода требуется сохранить код. Сохранить код?")
        if result: 
            File = File_Menu_SaveAs(TextBox)
            SelectedFile = File
        else: 
            return
    else: 
        File = SelectedFile

    run_button.config(state=DISABLED)  # Disable the button before execution
    try:
        with open(file=File, mode="r", encoding="utf-8") as File:
            exec(File.read() + '\ninput("Press Enter to exit...")\n')
    except Exception as e:
        showerror("Error", f"Произошла ошибка: {e}")
    finally:
        run_button.config(state=NORMAL)  # Re-enable the button after execution

# About Function
def About_Func():
    root.withdraw() 
    AboutRoot.deiconify()
    AboutRoot.mainloop()

# Main Function
def Init(File):
    global SelectedFile, root, AboutRoot
    if __name__ == "__main__":
        root = tk.Tk()
    else: root = Toplevel()
    if File:
        SelectedFile = File
        root.title(RootName + f' "{os.path.basename(SelectedFile)}"')
    root.title(RootName)
    root.geometry("820x500")
    root.option_add("*tearOff", False)
    
    AboutRoot = tk.Toplevel()
    AboutRoot.geometry("600x300")
    AboutRoot.resizable(False, False)
    AboutRoot.title("About LUT Editor")
    
    # Back Button in About Window
    def smallFunc():
        root.deiconify()
        AboutRoot.withdraw()
        
    backButton = Button(AboutRoot, text="Back", font="MonoLisa 10", command=smallFunc, width=10)
    backButton.pack(anchor=SE, side=BOTTOM, padx=[0, 10], pady=[0, 5])
    
    # Info Text in About Window
    InfoText = Label(AboutRoot, text="LUT Editor — это редактор файлов, разработанный на Python, который позволяет редактировать и сохранять Python-код. Программа может запускать файлы Python, если на компьютере установлен интерпретатор Python. Это делает LUT Editor удобным инструментом для разработки и тестирования Python-программ.", justify=LEFT, anchor=NW, font="MonoLisa 12", wraplength=500)
    InfoText.pack(anchor=NW)

    AboutRoot.withdraw()
    # Icon Setup
    try:
        root.iconbitmap(default=".\_internal\LUT_Editor.ico")
        AboutRoot.iconbitmap(default=".\_internal\LUT_Editor.ico")
    except:
        print("Icons not found")
    
    TextBox = ScrolledText(root, font="MonoLisa 12", wrap="none")
    if __name__ == "__main__":TextBox.insert("0.1", "print('Hello, world!')")
    else: TextBox.insert("0.1", open(SelectedFile,"r",encoding="utf-8").read())
    TextBox.pack(fill=BOTH, side=LEFT, expand=True, padx=[3, 3], pady=[3, 3])
    
    # File Menu
    File_Menu = tk.Menu()
    File_Menu.add_cascade(label="New", command=lambda: File_Menu_New(TextBox))
    File_Menu.add_cascade(label="Save", command=lambda: File_Menu_Save(TextBox))
    File_Menu.add_cascade(label="Save as", command=lambda: File_Menu_SaveAs(TextBox))
    File_Menu.add_cascade(label="Open", command=lambda: File_Menu_Open(TextBox))
    
    # Main Menu
    Main_Menu = tk.Menu()
    Main_Menu.add_cascade(label="File", menu=File_Menu)
    Main_Menu.add_cascade(label="About", command=lambda: About_Func())
    
    run_button = tk.Button(root, text="Run code", command=lambda: threading.Thread(target=File_Init, args=(TextBox, run_button)).start())
    run_button.pack(side=BOTTOM, padx=[3, 3], pady=[3, 3])
    
    root.config(menu=Main_Menu)
    
    root.mainloop()

# GUI Initialization
if __name__ == "__main__":
    Init(None)