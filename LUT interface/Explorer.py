# LUT Explorer 2025, version - 0.0.0-alpha by @offjjo

from tkinter import *; from tkinter import messagebox; from pathlib import Path; import os; import shutil; import Editor

currentDirectory = Path.cwd()
start_index = 0
selected_file = None
selected_frame = None
moving_mode = False
copy_mode = False
explorer_frame = None
move_button = None
copy_button = None
rename_button = None
rename_frame = None

def EditFile():
    if selected_file:Editor.Init(selected_file)

def SelectClear():
    global selected_frame
    try:
        if selected_frame is not None:
            selected_frame.configure(bg="#ffffff")
            for widget in selected_frame.winfo_children():
                widget.configure(bg="#ffffff")
    except:
        print("Hi")

def CancelAllAction():
    global selected_file, selected_frame, moving_mode, move_button, rename_frame, rename_button
    move_button.configure(text="Move file")
    rename_button.configure(text="Rename")
    if rename_frame:
        rename_frame.destroy()
        rename_frame = None
    selected_file = None
    moving_mode = False
    SelectClear()
    selected_frame = None
    
def CopyFile(Button):
    global selected_file, currentDirectory, copy_mode, explorer_frame, moving_mode
    if selected_file and not moving_mode and not copy_mode:
        copy_mode = True
        Button.configure(text="Copy to current direction")
        return
    if os.path.samefile(selected_file, currentDirectory): return
    Button.configure(text="Copy file")
    try:
        if os.path.isfile(selected_file):
            shutil.copy(selected_file, currentDirectory)
        else:
            folder_name = os.path.basename(selected_file)
            new_destination = os.path.join(currentDirectory, folder_name)
            shutil.copytree(selected_file, new_destination)
            print("Director")
    except: pass
    CancelAllAction()
    LoadFilesInExplorer(explorer_frame)
    copy_mode = False

def RemoveFile():
    global selected_file
    if not messagebox.askyesno("Удаление файла", f"Вы уверены что хотите безвозвратно удалить этот файл?\n{selected_file}"):
        SelectClear()
        CancelAllAction()
        return
    if os.path.isdir(selected_file):
        shutil.rmtree(selected_file)
    else: os.remove(selected_file)
    SelectClear()
    CancelAllAction()
    LoadFilesInExplorer(explorer_frame)

def MoveFile(Button):
    global selected_file, currentDirectory, moving_mode, explorer_frame
    if selected_file and not moving_mode:
        moving_mode = True
        Button.configure(text="Move to current direction")
        return
    if os.path.samefile(selected_file, currentDirectory): return
    Button.configure(text="Move file")
    try:
        shutil.move(selected_file, currentDirectory)
    except: pass
    CancelAllAction()
    LoadFilesInExplorer(explorer_frame)
    moving_mode = False

def RenameFile():
    if not selected_file: return
    print(selected_file)
    global rename_frame
    if rename_frame:
        new_name = rename_frame.get()
        if not new_name or new_name == "": return
        os.rename(selected_file, new_name)
        rename_frame.destroy()
        rename_frame = None
        SelectClear()
        CancelAllAction()
        LoadFilesInExplorer(explorer_frame)
        rename_button.configure(text="Rename")
        return
    RenameFrame = Entry(selected_frame, bg="#ffffff", font=10)
    RenameFrame.pack(fill=X, side=LEFT)
    RenameFrame.insert(0, os.path.basename(selected_file))
    rename_frame = RenameFrame
    rename_button.configure(text="Confirm rename")

def CreateFile():
    print("CreatingFile")
    result = messagebox.askyesnocancel("Creating file", "Создать папку или файл?\n(yes - файл, no - Папка)")
    print(result)
    if result == True:
        with open(str(currentDirectory)+"/NewFile", "w"):
            pass
        print("File created")
        LoadFilesInExplorer(explorer_frame)
    elif result == False:
        os.makedirs("NewFolder")
        print("Folder created")
        LoadFilesInExplorer(explorer_frame)
    else: pass

def GoToPath(newPath, Explorer_Frame):
    global currentDirectory
    try:
        currentDirectory = newPath
        LoadFilesInExplorer(Explorer_Frame)
    except: messagebox.showerror("Path error", "Неверный путь")

def go_to_parent_directory(Parent_Frame):
    global currentDirectory
    currentDirectory = Path(currentDirectory)
    if currentDirectory.parent != currentDirectory:  # Проверяем, что не находимся в корневой директории
        currentDirectory = currentDirectory.parent
        global start_index
        start_index = 0  # Сброс индекса при переходе на родительскую директорию
        LoadFilesInExplorer(Parent_Frame)

def GetFilesInCurrentDirectory(path):
    return [f for f in Path(path).iterdir()]

def get_file_type(file):
    if os.path.isdir(file):
        return "D"  # Директория
    elif os.path.isfile(file):
        return "F"  # Файл
    return "U"  # Неизвестный

def is_executable(file):
    return os.access(file, os.X_OK)

def sort_files(files):
    return sorted(files, key=lambda f: (get_file_type(f), os.path.basename(f), not is_executable(f)))

def LoadFilesInExplorer(Parent_Frame):
    global selected_frame  # Делаем переменную глобальной
    children = Parent_Frame.winfo_children()
    
    # Очищаем фрейм explorer
    for frame in children:
        if isinstance(frame, Frame):
            frame.destroy()
    
    # Получаем файлы
    files = GetFilesInCurrentDirectory(currentDirectory)
    sorted_files = sort_files(files)

    if not sorted_files:  # Если нет файлов, просто выходим
        return
    
    for file in sorted_files[start_index:]:
        # Эффект границы
        BorderFrame = Frame(Parent_Frame, bg="#858585", height=31)
        BorderFrame.pack_propagate(False)
        BorderFrame.pack(side=TOP, fill=X)
        
        # Фрейм с данными файла
        FileFrame = Frame(BorderFrame, bg="#ffffff", height=30)
        FileFrame.pack_propagate(False)
        FileFrame.pack(fill=X)
        
        # Данные
        FileType = "Unknown"
        if file.is_dir():
            FileType = "📁 D -"
        elif file.is_file():
            FileType = "📄 F -"
        
        Executable = "Unknown"
        if os.access(file, os.X_OK):
            Executable = "*exec"
        else:
            Executable = "/notexec"

        # Результат
        result = f"{FileType}  {file.name}  {Executable}"
        
        # Запись данных в фрейм
        FileNameFrame = Label(FileFrame, bg="#ffffff", text=result, font=10)
        FileNameFrame.pack(fill=X, side=LEFT)
        
        # Функции для событий
        def on_enter(event, frame=FileFrame, innerframe=FileNameFrame):
            global selected_frame
            if frame != selected_frame:  # Если фрейм не выделен, изменяем цвет
                frame.configure(bg="#c4c4c4")
                innerframe.configure(bg="#c4c4c4")
            
        def on_leave(event, frame=FileFrame, innerframe=FileNameFrame):
            global selected_frame
            if frame != selected_frame:  # Если фрейм не выделен, возвращаем цвет
                frame.configure(bg="#ffffff")
                innerframe.configure(bg="#ffffff")

        def on_click(event, frame=FileFrame, innerframe=FileNameFrame, file=file):
            global selected_file, selected_frame, moving_mode, copy_mode
            if moving_mode or copy_mode: return
            selected_file = os.path.abspath(file)
            print(selected_file)
            
            # Снимаем выделение с предыдущего фрейма
            SelectClear()
            
            # Устанавливаем новый выделенный фрейм
            selected_frame = frame
            frame.configure(bg="#c4c4c4")
            innerframe.configure(bg="#c4c4c4")
        
        def on_double_click(event, frame=FileFrame, innerframe=FileNameFrame, file=file):
            if file.is_dir():
                global currentDirectory  # Указываем, что изменяем глобальную переменную
                currentDirectory = file  # Обновляем currentDirectory на новый путь
                global start_index
                start_index = 0
                LoadFilesInExplorer(Parent_Frame)  # Загружаем файлы в новом каталоге
            elif file.is_file():
                print("Открытие файла:", file)
        
        # Привязываем события к фрейму
        FileFrame.bind("<Enter>", on_enter)   # Наведение мыши
        FileFrame.bind("<Leave>", on_leave)    # Покидание мыши
        FileFrame.bind("<Button-1>", on_click) # Нажатие левой кнопкой мыши
        FileFrame.bind("<Double-Button-1>", on_double_click)
        FileNameFrame.bind("<Button-1>", on_click) # Нажатие левой кнопкой мыши
        FileNameFrame.bind("<Double-Button-1>", on_double_click)

def PageDownFunc(Frame):
    global start_index
    start_index += 1
    LoadFilesInExplorer(Frame)
    
def PageUpFunc(Frame):
    global start_index
    if start_index > 0:
        start_index -= 1
    LoadFilesInExplorer(Frame)

def Init():
    if __name__ == "__main__":
        ExplorerRoot = Tk()
        ExplorerRoot.title("LUT Explorer")
    else:
        ExplorerRoot = Toplevel()
        ExplorerRoot.title("Explorer")
    ExplorerRoot.geometry("900x500")
    
    # Основные панели управления Explorer
    MainFrame = Frame(ExplorerRoot, bg="#212121")
    MainFrame.pack(fill=BOTH, expand=True)
    
    PathFrame = Frame(MainFrame, bg="#4d348c", height=35)
    PathFrame.pack_propagate(False)
    PathFrame.pack(side=TOP, fill=X)
    
    ToolFrame = Frame(MainFrame, bg="#347e8c", height=35)
    ToolFrame.pack_propagate(False)
    ToolFrame.pack(side=TOP, fill=X)
    
    SidePanelFrame = Frame(MainFrame, bg="#348c5a", width=150)
    SidePanelFrame.pack_propagate(False)
    SidePanelFrame.pack(side=LEFT, fill=Y)
    
    ExplorerFrame = Frame(MainFrame, bg="#6f8c34")
    ExplorerFrame.pack_propagate(False)
    ExplorerFrame.pack(side=LEFT, fill=BOTH, expand=True)
    
    global explorer_frame
    explorer_frame = ExplorerFrame
    
    # Кнопки и ввод текста
    # Фрейм "Пути"
    paddingX = 3
    
    BackButton = Button(PathFrame, text="<- Back", command=lambda: go_to_parent_directory(ExplorerFrame), relief=FLAT)
    BackButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    UpdateButton = Button(PathFrame, text="🔄 Refresh", command=lambda: LoadFilesInExplorer(ExplorerFrame), relief=FLAT, bg="#4CAF50", fg="white")
    UpdateButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    PathEntry = Entry(PathFrame, width=110)
    PathEntry.pack(side=LEFT, fill=X, padx=[20, 10])
    
    PathEntry.insert(0, currentDirectory)
    
    GoToPathButton = Button(PathFrame, text="Confirm", command=lambda: GoToPath(PathEntry.get(), ExplorerFrame), relief=FLAT)
    GoToPathButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    # Панель управления
    CancelButton = Button(ToolFrame, text="Cancel", command=lambda:CancelAllAction(), relief=FLAT)
    CancelButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    DeleteButton = Button(ToolFrame, text="Delete", command=lambda: RemoveFile(), relief=FLAT, bg="#e83a3a", fg="#ffffff")
    DeleteButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    MoveButton = Button(ToolFrame, text="Move file", command=lambda:MoveFile(MoveButton), relief=FLAT)
    MoveButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    CopyButton = Button(ToolFrame, text="Copy file", command=lambda:CopyFile(CopyButton), relief=FLAT)
    CopyButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    RenameButton = Button(ToolFrame, text="Rename", command=lambda:RenameFile(), relief=FLAT)
    RenameButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    CreateButton = Button(ToolFrame, text="Create", command=lambda:CreateFile(), relief=FLAT)
    CreateButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    EditButton = Button(ToolFrame, text="Edit file", command=lambda:EditFile(), relief=FLAT)
    EditButton.pack(side=LEFT, fill=X, padx=paddingX)
    
    # Глобализация переменных
    global move_button
    move_button = MoveButton
    
    global copy_button
    copy_button = CopyButton
    
    global rename_button
    rename_button = RenameButton
    
    # пролистывание
    PageUp = Button(MainFrame, text="↑\nUP", command=lambda: PageUpFunc(ExplorerFrame))
    PageUp.pack(side=TOP, fill=BOTH, expand=True)
    
    PageDown = Button(MainFrame, text="DOWN\n↓", command=lambda: PageDownFunc(ExplorerFrame))
    PageDown.pack(side=TOP, fill=BOTH, expand=True)

    # preload
    LoadFilesInExplorer(ExplorerFrame)
    
    ExplorerRoot.mainloop()
    
if __name__ == "__main__":
    Init()