# Интерфейсные кнопки
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import config

# Кнопки на табе с датагридом
def DrawDataButtons(frame):
    # Кнопка обновления данных
    frame.image_reload = ImageTk.PhotoImage(Image.open("images\\icons8-available-updates-30.png"))
    frame.refresh_button = tk.Button(
        frame.grid_icon_frame,
        image=frame.image_reload, 
        text = ' Загрузить журналы ',
        compound=tk.LEFT,
        cursor="hand2",
        command=frame.data_reload,
        name="data_reload",
        bd=0,
        height=40

    )
    frame.refresh_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)

    # Кнопка запуска запроса
    frame.image_refresh = ImageTk.PhotoImage(Image.open("images\\icons8-circled-play-30.png"))
    frame.refresh_button = tk.Button(
        frame.grid_icon_frame,
        image=frame.image_refresh, 
        text = ' Запустить запрос ',
        compound=tk.LEFT,
        cursor="hand2",
        command=frame.data_refresh,
        name="data_refresh",
        bd=0,
        height=40

    )
    frame.refresh_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)

    # Кнопка Экспорт в CSV
    frame.image_export = ImageTk.PhotoImage(Image.open("images\\icons8-export-csv-green-30.png"))
    frame.export_button = tk.Button(
        frame.grid_icon_frame, 
        image=frame.image_export, 
        text=" Экспорт в CSV ",
        compound=tk.LEFT,
        cursor="hand2",
        command=frame.SaveCSV,
        name="data_export",
        bd=0,
        height=40,
    )
    frame.export_button.pack(side=tk.LEFT, padx=0, ipadx=0)

# Кнопки на табе с выбором файлов
def DrawFilesButtons(frame):
    frame.image_select = ImageTk.PhotoImage(Image.open("images\\icons8-add-list-30.png"))
    # кнопка выбора логов
    frame.select_button = tk.Button(
        frame.files_icon_frame, 
        image=frame.image_select, 
        text=" Загрузить журналы",
        cursor="hand2",
        command=frame.select_files,
        name="select_files",
        compound=tk.LEFT,
        bd=0,
        height=40,
        #width = 150
    )
    frame.select_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)

    frame.image_clear_selection = ImageTk.PhotoImage(Image.open("images\\icons8-delete-row-30.png"))
    # Удалить выбранные логи ----------
    frame.clear_selection_button = tk.Button(
        frame.files_icon_frame, 
        image=frame.image_clear_selection, 
        text=" Удалить выбранные",
        cursor="hand2",
        command=frame.clear_selected_files,
        name="clear_selected_files",
        compound=tk.LEFT,
        bd=0,
        height=40,
        #width = 150
    )
    frame.clear_selection_button.pack(side=tk.LEFT, padx=0, ipadx=5)

    # Удалить все ------------
    frame.image_clear = ImageTk.PhotoImage(Image.open("images\\icons8-clear-30.png"))
    # кнопка
    frame.clear_button = tk.Button(
        frame.files_icon_frame, 
        image=frame.image_clear, 
        text=" Удалить все",
        cursor="hand2",
        command=frame.clear_files,
        name="clear_files",
        compound=tk.LEFT,
        bd=0,
        height=40,
    )
    frame.clear_button.pack(side=tk.LEFT, padx=0, ipadx=5)

    label = ttk.Label(frame.files_icon_frame, text="| Тип журналов: ")
    label.pack(side=tk.LEFT, padx=0, ipadx=5)

    # Комбобокс. Выбор типа журнала
    frame.logtype_select = ttk.Combobox(frame.files_icon_frame, textvariable=frame.LogType, state='readonly')
    frame.logtype_select['values'] = frame.LogTypes
    frame.logtype_select.set(frame.LogType)
    frame.logtype_select.pack(side=tk.LEFT, padx=0, ipadx=5)
    frame.logtype_select.bind("<<ComboboxSelected>>", frame.SelectLogType)

    # Комбобокс. Выбор разделителя
    label = ttk.Label(frame.files_icon_frame, text="| Разделитель для CSV: ")
    label.pack(side=tk.LEFT, padx=0, ipadx=5)

    frame.delimiter_select = ttk.Combobox(frame.files_icon_frame, text=frame.Delimiter, state='readonly')
    frame.delimiter_select['values'] = config.DELIMITERS
    frame.delimiter_select.set(frame.Delimiter)
    frame.delimiter_select.pack(side=tk.LEFT, padx=0, ipadx=5)
    frame.delimiter_select.bind("<<ComboboxSelected>>", frame.SelectDelimiter)

    # действия кнопок

def data_export():
        print("Экспорт в CSV")

def data_reload(dataobject):
     pass

def data_refresh(dataobject):
    pass
