# Интерфейсные кнопки
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import config, img

# Кнопки на табе с датагридом
def DrawDataButtons(frame):
    # Кнопка обновления данных
    frame.image_reload = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.data_reload))))
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
    frame.image_refresh = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.data_refresh))))
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
    #frame.image_export = ImageTk.PhotoImage(Image.open("images\\icons8-export-csv-green-30.png"))
    frame.image_export = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.SaveCSV))))
    frame.export_button = tk.Button(
        frame.grid_icon_frame, 
        image=frame.image_export, 
        text=" Экспорт в CSV ",
        compound=tk.LEFT,
        cursor="hand2",
        command=frame.file_manager.save_csv,
        name="data_export",
        bd=0,
        height=40,
    )
    frame.export_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)

    # Кнопка хелп
    frame.image_help = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.help))))
    frame.help_button = tk.Button(
        frame.grid_icon_frame, 
        image=frame.image_help, 
        text=" Справка ",
        compound=tk.LEFT,
        cursor="hand2",
        command=frame.ShowHelp,
        name="data_help",
        bd=0,
        height=40,
    )
    frame.help_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)


# Кнопки на табе с выбором файлов
def DrawFilesButtons(frame):
    frame.image_select = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.select_files))))
    # кнопка выбора логов
    frame.select_button = tk.Button(
        frame.files_icon_frame, 
        image=frame.image_select, 
        text=" Добавить файлы",
        cursor="hand2",
        command=frame.file_manager.select_files,
        name="select_files",
        compound=tk.LEFT,
        bd=0,
        height=40,
        #width = 150
    )
    frame.select_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)

    frame.image_clear_selection = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.clear_selected_files))))
    # Удалить выбранные логи ----------
    frame.clear_selection_button = tk.Button(
        frame.files_icon_frame, 
        image=frame.image_clear_selection, 
        text=" Удалить выбранные",
        cursor="hand2",
        command=frame.file_manager.clear_selected_files,
        name="clear_selected_files",
        compound=tk.LEFT,
        bd=0,
        height=40,
        #width = 150
    )
    frame.clear_selection_button.pack(side=tk.LEFT, padx=0, ipadx=5)

    # Удалить все ------------
    frame.image_clear = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.clear_files))))
    # кнопка
    frame.clear_button = tk.Button(
        frame.files_icon_frame, 
        image=frame.image_clear, 
        text=" Удалить все",
        cursor="hand2",
        command=frame.file_manager.clear_files,
        name="clear_files",
        compound=tk.LEFT,
        bd=0,
        height=40,
    )
    frame.clear_button.pack(side=tk.LEFT, padx=0, ipadx=5)

    frame.DividerLabel1 = ttk.Label(frame.files_icon_frame, text="|")
    frame.DividerLabel1.pack(side=tk.LEFT, padx=(10,10))   

    label = ttk.Label(frame.files_icon_frame, text=config.LOG_TYPE)
    label.pack(side=tk.LEFT, padx=0, ipadx=2)

    # Комбобокс. Выбор типа журнала
    frame.logtype_select = ttk.Combobox(frame.files_icon_frame, textvariable=frame.LogType, state='readonly')
    frame.logtype_select['values'] = frame.LogTypes
    frame.logtype_select.set(frame.LogType)
    frame.logtype_select.pack(side=tk.LEFT, padx=0, ipadx=5)
    frame.logtype_select.bind("<<ComboboxSelected>>", frame.SelectLogType)

    frame.DividerLabel2 = ttk.Label(frame.files_icon_frame, text="|")
    frame.DividerLabel2.pack(side=tk.LEFT, padx=(10,10))   
    # Комбобокс. Выбор разделителя
    label = ttk.Label(frame.files_icon_frame, text=config.DELIMITER_CSV)
    label.pack(side=tk.LEFT, padx=0, ipadx=2)

    frame.delimiter_select = ttk.Combobox(frame.files_icon_frame, width=3, text=frame.Delimiter, state='readonly')
    frame.delimiter_select['values'] = config.DELIMITERS
    frame.delimiter_select.set(frame.Delimiter)
    frame.delimiter_select.pack(side=tk.LEFT, padx=0, ipadx=5)
    frame.delimiter_select.bind("<<ComboboxSelected>>", frame.SelectDelimiter)

    frame.DividerLabel3 = ttk.Label(frame.files_icon_frame, text="|")
    frame.DividerLabel3.pack(side=tk.LEFT, padx=(10,10))   
    # Коррекция таймзоны
    check = (frame.register(frame.TimezoneSet), "%P")
    label = ttk.Label(frame.files_icon_frame, text=config.TIMEZONE_CORRECTION)
    label.pack(side=tk.LEFT, padx=0, ipadx=2)
    frame.ZoneCorrection = ttk.Entry(frame.files_icon_frame, width=5, validate="focusout", validatecommand=check)
    frame.ZoneCorrection.insert(0, str(frame.Timezone))
    frame.ZoneCorrection.pack(side=tk.LEFT, padx=0, ipadx=5)
    # действия кнопок




def data_export():
    pass

def data_reload(dataobject):
     pass

def data_refresh(dataobject):
    pass
