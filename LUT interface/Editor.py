from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import *
from tkinter.messagebox import *
import os
import threading
import queue

# Global Variables
SelectedFile = None
root = None
AboutRoot = None
RootName = os.path.basename(__file__)
execution_thread = None
stop_event = threading.Event()
output_queue = queue.Queue()

# File Menu Functions
def File_Menu_New(TextBox):
    global SelectedFile
    TextBox.delete("1.0", END)
    SelectedFile = None
    root.title(RootName)

def File_Menu_Save(TextBox):
    global SelectedFile
    if SelectedFile is None:
        return File_Menu_SaveAs(TextBox)  # Если файла нет, вызываем Save As
    try:
        with open(SelectedFile, "w+", encoding="utf-8") as File:
            File.write(TextBox.get("1.0", END))
            root.title(RootName + f' "{os.path.basename(SelectedFile)}"')
    except Exception as e:
        showerror("Error", f"Ошибка сохранения файла: {e}")

def File_Menu_SaveAs(TextBox):
    global SelectedFile
    try:
        GetFile = asksaveasfilename(title="Выбор файла",
                                     confirmoverwrite=True,
                                     defaultextension="txt",
                                     initialfile="PythonFile.py")
        if GetFile:  # Проверяем, что файл был выбран
            with open(GetFile, "w+", encoding="utf-8") as File:
                File.write(TextBox.get("1.0", END))
                SelectedFile = GetFile
            root.title(RootName + f' "{os.path.basename(SelectedFile)}"')
    except Exception as e:
        showerror("Error", f"Ошибка сохранения файла: {e}")

def File_Menu_Open(TextBox):
    global SelectedFile
    try:
        OpenFile = askopenfilename()
        if OpenFile:  # Проверяем, что файл был выбран
            TextBox.delete("1.0", END)
            with open(OpenFile, "r", encoding="utf-8") as File:
                TextBox.insert("0.1", File.read())
            SelectedFile = OpenFile
            root.title(RootName + f' "{os.path.basename(SelectedFile)}"')  # Обновляем заголовок
    except Exception as e:
        showerror("Error", f"Ошибка открытия файла: {e}")

def execute_code(code):
    global stop_event
    stop_event.clear()  # Сбрасываем флаг остановки
    try:
        # Оборачиваем exec в функцию, чтобы использовать stop_event
        exec_code = code
        exec(exec_code)
    except Exception as e:
        output_queue.put(f"Ошибка выполнения кода: {e}")

def File_Init(TextBox, run_button):
    global execution_thread
    if len(TextBox.get("0.1", END)) == 0 or TextBox.get("0.1", END).isspace():
        return

    code = TextBox.get("1.0", END)
    run_button.config(state=DISABLED)  # Disable the button before execution

    # Запуск кода в отдельном потоке
    execution_thread = threading.Thread(target=execute_code, args=(code,))
    execution_thread.start()

    # Запуск потока для обновления вывода
    root.after(100, check_output)

def check_output():
    while not output_queue.empty():
        output = output_queue.get()
        print(output)  # Выводим в консоль, можно добавить в текстовое поле
    if execution_thread.is_alive():
        root.after(100, check_output)  # Проверяем вывод каждые 100 мс
    else:
        run_button.config(state=NORMAL)  # Re-enable the button after execution

def stop_code():
    global stop_event
    stop_event.set()  # Устанавливаем флаг остановки

# About Function
def About_Func():
    root.withdraw() 
    AboutRoot.deiconify()
    AboutRoot.mainloop()

# Main Function
def Init(File):
    global SelectedFile, root, AboutRoot, run_button
    if __name__ == "__main__":root = tk.Tk()
    else:root = tk.Toplevel()
    print(File)
    if File != None:
        SelectedFile = File
        root.title(RootName + f' "{os.path.basename(File)}"')
    else:root.title(RootName)
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
    
    TextBox = ScrolledText(root, font="MonoLisa 12", wrap="none")
    if __name__ == "__main__": TextBox.insert("0.1", "print('Hello, world!')")
    else:
        if File != None:
            with open(file=File, mode="r", encoding="utf-8") as File:
                TextBox.insert("0.1", File.read())
    TextBox.pack(fill=BOTH, side=BOTTOM, expand=True, padx=[3, 3], pady=[3, 3])
    
    # Create buttons instead of menu
    button_frame = Frame(root)
    button_frame.pack(side=LEFT, fill=X)

    new_button = Button(button_frame, text="New", command=lambda: File_Menu_New(TextBox))
    new_button.pack(side=LEFT, padx=2, pady=5)

    save_button = Button(button_frame, text="Save", command=lambda: File_Menu_Save(TextBox))
    save_button.pack(side=LEFT, padx=2, pady=5)

    save_as_button = Button(button_frame, text="Save As", command=lambda: File_Menu_SaveAs(TextBox))
    save_as_button.pack(side=LEFT, padx=2, pady=5)

    open_button = Button(button_frame, text="Open", command=lambda: File_Menu_Open(TextBox))
    open_button.pack(side=LEFT, padx=2, pady=5)

    about_button = Button(button_frame, text="About", command=lambda: About_Func())
    about_button.pack(side=LEFT, padx=2, pady=5)

    run_button = tk.Button(root, text="Run code", command=lambda: File_Init(TextBox, run_button))
    run_button.pack(side=RIGHT, padx=[3, 3], pady=[3, 3])

    stop_button = tk.Button(root, text="Stop code", command=stop_code)
    stop_button.pack(side=RIGHT, padx=[3, 3], pady=[3, 3])

    root.mainloop()

# GUI Initialization
if __name__ == "__main__":
    Init(None)
