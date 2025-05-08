import re, os, site
module_path = os.path.join(os.path.join(os.getcwd(), 'mod'))
site.addsitedir(module_path)
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
#import tkinter.font as tkFont
from time import time
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO

#моё
import programstate, btn, ui, loaders, config, img, filemanager

class LogExplorer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # переменные для перетаскивания границы между окнами
        self.dragging = False
        self.start_y = 0

        self.column_names = []
        self.LogType = config.DEFAULT_LOG_TYPE
        self.LogTypes = config.LOG_TYPES 
        self.Delimiter = config.DEFAULT_DELIMITER
        self.Timezone = config.DEFAULT_TIMEZONE
        #self.filelist =[] #сюда будем складывать списки логов. Список передадим поларсу
        self.file_manager = filemanager.FileManager(self)
        self.json_path = "" #здесь будут храниться данные о состоянии программы (конфиг, текущие данные и тп)
        self.sort_direction = {}
        self.last_height = config.WINDOW_HEIGHT 
        self.RequestSQL = config.DEFAULT_SQL
        self.NumberLabelText = tk.StringVar()
        self.NumberLabelText.set("| Результат: ")
        self.RefreshLabelText = tk.StringVar()
        self.RefreshLabelText.set("| Запрос: ")
        programstate.init_file(self)
        programstate.LoadState(self) # загрузка значений в контролы из json        
        self.setup_ui()

    def setup_ui(self):
        self.tabControl = ttk.Notebook(self.parent) # ноутбук = хранилище табов
        self.tab_front = ttk.Frame(self.tabControl) # Таб для грида. создание
        self.tab_front.pack_propagate(0)
        self.tab_files = ttk.Frame(self.tabControl) # Таб для списка файлов. создание
        self.tabControl.add(self.tab_front, text =config.DATATAB_LABEL) # помещаем таб грида в ноутбук
        self.tabControl.add(self.tab_files, text =config.FILESTAB_LABEL) # помещаем таб списка файлов в ноутбук
        self.tabControl.pack(expand = 1, fill =tk.BOTH) 

        ui.SetupIconFrame(self)     # фрейм для иконок на табе "Данные"
        ui.SetupDataFrame(self)     # Фрейм для вывода данных
        ui.SetupDividerFrame(self)  # Подвижный разделитель между фреймами
        ui.SetupRequestFrame(self)  # Фрейм для вывода данных
        btn.DrawDataButtons(self)   # Кнопки на табе с данными
        ui.SetupDataGrid(self)      # Treeview с результатами запроса
        ui.SetupRequestEditor(self) # Окно редактора запроса
        self.parent.update()
        self.total_height = self.tab_front.winfo_height()
        self.tree_frame.configure(height=self.total_height/2)
        self.request_frame.configure(height=self.total_height/2)
        self.parent.bind("<Configure>", self.on_window_resize)
        # ============================================================================================================================================
        # Контролы таба выбора файлов
        self.files_icon_frame = tk.Frame(self.tab_files, height=50)
        self.files_icon_frame.pack(fill=tk.X, padx=10, pady=10)

        # Фрейм для списка файлов
        self.files_frame = tk.Frame(self.tab_files)
        self.files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)    

        btn.DrawFilesButtons(self)

        # Заголовок списка файлов
        self.files_label = tk.Label(self.files_frame, text=config.SELECTED_LOGS, anchor="w")
        self.files_label.pack(fill=tk.X, pady=(0, 5))

        # Create a frame for the list and scrollbar
        self.list_frame = tk.Frame(self.files_frame)
        self.list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for the list
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox to display selected files
        self.files_listbox = tk.Listbox(
            self.list_frame,
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.EXTENDED
        )
        self.file_manager.setup_listbox(self.files_listbox)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure the scrollbar
        self.scrollbar.config(command=self.files_listbox.yview)

    # ==============================================================================================================
    # Кнопочные функции
    def button_clicked(self):
        print("Button")

    # удаление всех файлов из списка журналов
    def clear_files(self):
        self.file_manager.clear_files()

    # удаление выбранных файлов из списка журналов
    def clear_selected_files(self):
        self.file_manager.clear_selected_files()

    # Вызов окна диалога выбора файлов и добавление выбранного в список с исключением дубликатов
    def select_files(self):
        self.file_manager.select_files()

    # подключает файлы, указанные в списке "Выбранные журналы" и грузит минимальную выборку (дефолтный SQL) 
    def data_reload(self):
        self.LoadData()
        self.clear_treeview()
        self.PopulateDataGrid()

    # сохранение результата выборки в файле
    def SaveCSV(self):
        if hasattr(self, 'df'):
            self.file_manager.save_csv(self.df)

    def ShowHelp(self):
        messagebox.showinfo("Краткая справка", config.HELP_TEXT)

    def SelectDelimiter(self, event):
        self.Delimiter = self.delimiter_select.get()
        programstate.save_data(self)
    # Функция сортировки. Клик по колонке - сортировка по ней. повторный клик - сортировка в обратном порядке
    def sort_treeview_column(self, col_name):
        start = time()
        current_sort = self.sort_direction.get(col_name, 'ascending')
        item_list = [(self.tree.item(item, "text"), self.tree.item(item, "values")) for item in self.tree.get_children("")]
        col_index = self.df.columns.index(col_name)
        ItemType = self.df.dtypes[col_index]
        if ItemType.is_numeric():
            key_func = lambda x: int(x[col_index]) 
        elif ItemType == 'String':
            key_func = lambda x: x[col_index].lower()
        else: 
            key_func = lambda x: x[col_index]

        if current_sort == 'ascending':
            sorted_data = sorted(item_list, key=lambda x: key_func(x[1]), reverse=True)
            self.sort_direction[col_name] = 'descending'
        else:
            sorted_data = sorted(item_list, key=lambda x: key_func(x[1]))
            self.sort_direction[col_name] = 'ascending'
        for item in self.tree.get_children(""):
            self.tree.delete(item)
        for item_id, values in sorted_data:
            self.tree.insert("", tk.END, text=item_id, values=values)
        
        #column_headings = [] - остатки старого кода
        i = 0
        for col in self.df.columns:
            if col == col_name:
                direction = " ↓" if current_sort ==  'ascending' else " ↑"
                self.tree.heading(i, text=f"{col_name}{direction}")
            else:
                self.tree.heading(i, text = col)
            i += 1
        end = time() - start
    # Выборка данных из списка журналов. Вызывает конкретную функцию загрузки в зависимости от типа журнала
    def LoadData(self):
        if len(self.file_manager.get_filelist()) < 1:
            messagebox.showerror(title="Не выбраны журналы", message="Выберите файлы на закладке 'Выбор журналов'")
            return
        start = time()
        self.TimeLabel['text'] = "Загрузка..."
        match self.LogType:
            case "IIS Log":
                loaders.LoadDataIIS(self)
            case "Exchange Log":
                loaders.LoadDataExchange(self)
            case "CSV":
                loaders.LoadDataCSV(self)
            case "Proxy":
                loaders.LoadDataProxy(self)
            case _:
                messagebox.showerror("Ошибка", "Не установлен тип журнала")
        end = time() - start
        TimeString = "Время загрузки: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60)
        self.TimeLabel['text'] = TimeString   

    def on_window_resize(self, event):
        # Обработка изменения размера основного окна
        ratio = 1
        constframes = self.grid_icon_frame.cget('height')+ self.divider_frame.cget('height')
        #return
        if event.widget == self.parent:
            if hasattr(self, 'last_height') and self.last_height > 0:
                if (self.last_height - constframes) > 0:
                    ratio = (self.parent.winfo_height() - constframes) / (self.last_height - constframes)
                else:
                    ratio = 0.5
                # Обновляем размеры с сохранением пропорций
                request_height = int(self.request_frame.winfo_height() * ratio)
                tree_height = int(self.tree_frame.winfo_height() * ratio)
                # Применяем новые размеры
                self.tree_frame.configure(height=tree_height)
                self.request_frame.configure(height=request_height)
            # Запоминаем текущую высоту для следующего пересчета
            self.last_height = self.parent.winfo_height()

    def filter_non_comment_lines(self, input_list):
        # Создаем пустой список для результата
        result_list = []
        # Проходим по каждой строке в исходном списке
        for line in input_list:
            # Проверяем, не начинается ли строка с символа '#'
            if not line.strip().startswith('#'):
                line = self.remove_comments(line)
                result_list.append(line)
        
        return result_list

    def remove_comments(self, input_string):
        # Регулярное выражение для поиска комментариев вида /*comment*/
        pattern = r'/\*.*?\*/'
        result = re.sub(pattern, '', input_string)
        return result

    def TimezoneSet(self, TZVal):
        if re.match("^[+-]{0,1}0{0,1}(?:2[0-3]{0,1}|1{0,1}[0-9]{0,1})$", TZVal):
            self.Timezone = int(TZVal)
            programstate.save_data(self)
            return True
        else:
            messagebox.showerror(title=config.WRONG_TIMEZONE_HEADER, message=config.WRONG_TIMEZONE)
            self.ZoneCorrection.delete(0, tk.END)
            self.ZoneCorrection.insert(0, str(self.Timezone))
            return False
        
    # запускает выборку с SQL-запросом из окна редактора запроса
    def data_refresh(self):
        self.RequestSQL = self.text.get("1.0", "end")
        tempSQLArray = self.RequestSQL.split("\n")
        tempSQLArray = self.filter_non_comment_lines(tempSQLArray)
        RequestSQL = ' '.join(tempSQLArray).strip()
        if not hasattr(self, 'LogData'):
            if messagebox.askyesno(title="Данные не загружены", message="Журналы не загружены.Загрузить их сейчас?"):
                self.data_reload()
            else:
                return    

        self.NumberLabelText.set("| Результат: ")
        self.RefreshLabelText.set("| Обработка запроса...")
        try:
            start = time()
            self.df = self.ctx.execute(RequestSQL)
            end = time() - start
            RefreshTime = "| Время обработки: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60)
            self.RefreshLabelText.set(RefreshTime)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обработка запроса: {str(e)}")
            return
        self.clear_treeview()
        self.PopulateDataGrid()

    # очистка окна результатов
    def clear_treeview(self):
        start = time()
        for item in self.tree.get_children():
            self.tree.delete(item)
        end = time() - start

    def SelectLogType(self, event):
        self.LogType = self.logtype_select.get()
        programstate.save_data(self)

    # вывод датафрейма на экран 
    def PopulateDataGrid(self):
        if not hasattr(self, 'df'):
            return
        #Рисуем статус запроса
        ResultNum = str(self.df.height)
        ResultLastNum = ResultNum[-1:]
        match ResultLastNum:
            case "1":
                strings = "строка"
            case "1" | "2" | "3" | "4":
                strings = "строки"
            case _:
                strings = "строк"
        limit = ""
        if self.df.height > config.SHOW_LIMIT:
            limit = " Показаны первые " + str(config.SHOW_LIMIT) + "."
        ResultString = "| Результат: " + ResultNum + " " + strings + "." + limit
        self.NumberLabelText.set(ResultString)
        self.tree['columns'] = self.df.columns # self.LogData.columns - список с перечислением имен полей датафрейма. self.tree['columns'] - кортеж из имен колонок treeview
        for col in self.df.columns:
            self.tree.heading(col, text=col, command=lambda col=col: self.sort_treeview_column(col))
            self.tree.column(col, width= 80, minwidth=80, stretch=0)  # Стандартная ширина
        # Добавляем строки
        for idx, row in enumerate(self.df.iter_rows()):
            # Преобразуем значения в строки для отображения
            values = []
            for value in row:
                if isinstance(value, datetime):
                    values.append(value.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    values.append(str(value))
            
            self.tree.insert('', tk.END, text=str(idx), values=values)
            if(idx>10000):
                break

def main():
    splash_root.destroy()
    root = tk.Tk()
    # Создание главного окна
    # Центрируем на экране
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - config.WINDOW_WIDTH) // 2
    y = (screen_height - config.WINDOW_HEIGHT)  // 2
    root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}")    
    root.title(config.PROGRAM_NAME)
    root.resizable(True, True)
    root.update_idletasks()
    #root.default_font = tkFont.nametofont("TkDefaultFont")
    #root.default_font.configure(size=10)
    app = LogExplorer(root)
    
#    root.mainloop()

splash_root = tk.Tk()
# Центрируем на экране
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()
x = (screen_width - config.SPLASH_WIDTH) // 2
y = (screen_height - config.SPLASH_HEIGHT)  // 2
splash_root.geometry(f"{config.SPLASH_WIDTH}x{config.SPLASH_HEIGHT}+{x}+{y}")    

splash_root.overrideredirect(True)
#splash_root.attributes('-alpha',0.5)
splash_root.wm_attributes("-transparentcolor", config.SPLASH_BG_COLOR)
splash_root.image_splash = ImageTk.PhotoImage(Image.open(BytesIO(img.b64_to_bin(img.splash))))
splash_label = tk.Label(splash_root, bg=config.SPLASH_BG_COLOR, image=splash_root.image_splash)

splash_label.pack()
splash_root.after(config.SPLASH_DISPLAY_TIME, main)

tk.mainloop()

#if __name__ == "__main__":
#    main()

