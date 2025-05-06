# listbox https://metanit.com/python/tkinter/2.12.php

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import random, string, os, programstate
from datetime import datetime, timedelta


class SortableDataGrid(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.generate_sample_data()
        self.populate_treeview()
        self.filelist =[] #сюда будем складывать списки логов. Список передадим поларсу
        json_path = "" #здесь будут храниться данные
        programstate.init_file(self)
        programstate.LoadState(self) # загрузка значений в контролы из json

    def setup_ui(self):
        # ноутбук = хранилище табов
        self.tabControl = ttk.Notebook(self.parent)
        self.tab_grid = ttk.Frame(self.tabControl) 
        self.tab_files = ttk.Frame(self.tabControl) 
        self.tabControl.add(self.tab_grid, text ='Данные') 
        self.tabControl.add(self.tab_files, text ='Выбор журналов') 
        self.tabControl.pack(expand = 1, fill ="both") 
  
        # фрейм для иконок на табе "Данные"
        self.grid_icon_frame = tk.Frame(self.tab_grid, height=50)
        self.grid_icon_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Фрейм для вывода данных
        self.tree_frame = tk.Frame(self.tab_grid)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)    

        # ================================================================================================
        # Кнопки на табе с данными

        # Кнопка обновления данных
        self.image_refresh = ImageTk.PhotoImage(Image.open("images/icons8-available-updates-30.png"))
        self.refresh_button = tk.Button(
            self.grid_icon_frame,
            image=self.image_refresh, 
            text = ' Обновить данные ',
            compound=tk.LEFT,
            cursor="hand2",
            command=self.data_refresh,
            name="data_refresh",
            bd=0,
            height=40

        )
        self.refresh_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)

        # Кнопка Экспорт в CSV
        self.image_export = ImageTk.PhotoImage(Image.open("images/icons8-export-csv-green-30.png"))
        self.export_button = tk.Button(
            self.grid_icon_frame, 
            image=self.image_export, 
            text=" Экспорт в CSV ",
            compound=tk.LEFT,
            cursor="hand2",
            command=self.data_export,
            name="data_export",
            bd=0,
            height=40,
        )
        self.export_button.pack(side=tk.LEFT, padx=0, ipadx=0)

        # ================================================================================================
        # грид с данными        
        # Create scrollbars
        self.vsb = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        self.hsb = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        
        # Configure the treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                                height=20, selectmode="extended", 
                                yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        # Set column headings
        self.tree.heading("#0", text="ID")
        self.tree.column("#0", width=50, minwidth=50)
        
        column_names = ["Name", "Department", "Position", "Age", "Salary", 
                       "Start Date", "Performance", "Projects", "Email", "Status"]
        
        for i, col_name in enumerate(column_names, 1):
            self.tree.heading(i, text=col_name, 
                             command=lambda _col=i: self.sort_treeview_column(_col))
            self.tree.column(i, width=100, minwidth=50)
        
        # Add the treeview and scrollbars to the frame
        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb.grid(row=1, column=0, sticky='ew')
        
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Variables for sorting
        self.sort_column = None
        self.sort_reverse = False

        # ============================================================================================================================================
        # Контролы таба выбора файлов
        self.files_icon_frame = tk.Frame(self.tab_files, height=50)
        self.files_icon_frame.pack(fill=tk.X, padx=10, pady=10)

        # Фрейм для списка файлов
        self.files_frame = tk.Frame(self.tab_files)
        self.files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)    

        # Выбор файлов ----------
        self.image_select = ImageTk.PhotoImage(Image.open("images/icons8-add-list-30.png"))
        # кнопка
        self.select_button = tk.Button(
            self.files_icon_frame, 
            image=self.image_select, 
            text=" Загрузить журналы",
            cursor="hand2",
            command=self.select_files,
            name="select_files",
            compound=tk.LEFT,
            bd=0,
            height=40,
            #width = 150
        )
        self.select_button.pack(side=tk.LEFT, padx=(10,0), ipadx=5)

        # Удалить выбранные ----------
        self.image_clear_selection = ImageTk.PhotoImage(Image.open("images/icons8-delete-row-30.png"))
        # кнопка
        self.clear_selection_button = tk.Button(
            self.files_icon_frame, 
            image=self.image_clear_selection, 
            text=" Удалить выбранные",
            cursor="hand2",
            command=self.clear_selected_files,
            name="clear_selected_files",
            compound=tk.LEFT,
            bd=0,
            height=40,
            #width = 150
        )
        self.clear_selection_button.pack(side=tk.LEFT, padx=0, ipadx=5)

        # Удалить все ------------
        self.image_clear = ImageTk.PhotoImage(Image.open("images/icons8-clear-30.png"))
        # кнопка
        self.clear_button = tk.Button(
            self.files_icon_frame, 
            image=self.image_clear, 
            text=" Удалить все",
            cursor="hand2",
            command=self.clear_files,
            name="clear_files",
            compound=tk.LEFT,
            bd=0,
            height=40,
            #width = 150
        )
        self.clear_button.pack(side=tk.LEFT, padx=0, ipadx=5)

        # Заголовок списка файлов
        self.files_label = tk.Label(self.files_frame, text="Выбранные журналы:", anchor="w")
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
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure the scrollbar
        self.scrollbar.config(command=self.files_listbox.yview)

    # ==============================================================================================================
    # Кнопочные функции

    def icon_clicked(self, icon_name):
        print(f"{icon_name} icon clicked")
        if icon_name == "refresh":
            self.generate_sample_data()
            self.clear_treeview()
            self.populate_treeview()
    
    def data_export(self):
        print("Экспорт в CSV")

    def button_clicked(self):
        print("Button")

    def clear_files(self):
        print("Удалить все журналы")
        self.files_listbox.delete(0, tk.END)
        self.filelist.clear()
        programstate.save_data(self)

    def clear_selected_files(self):
        print("Удалить выбранные журналы")
        ListToDelete = self.files_listbox.curselection()
        print(ListToDelete)
        for item in reversed(ListToDelete): # в обратном порядке потому, что при удалении элемента, список пересчитывается и индексы смещаются
            self.files_listbox.delete(item)
        print(type(self.filelist))
        self.filelist.clear()
        for i in self.files_listbox.get(0, self.files_listbox.size()):
            self.filelist.append(i)
        print(self.filelist)
        programstate.save_data(self)


    def select_files(self):
            filepaths = filedialog.askopenfilenames(
                title="Выбор журналов",
                filetypes=(
                    ("Все файлы", "*.*"),
                    ("Журналы", "*.log"),
                )
            )
            if filepaths != "":
                # делаем set, чтобы исключить дубликаты файлов
                temp_list = set()
                for i in self.filelist:
                    temp_list.add(i)
                self.files_listbox.delete(0, tk.END)
                self.filelist.clear()
                for filepath in filepaths:
                    temp_list.add(filepath)
                self.filelist = list(temp_list)
                for i in temp_list:
                    self.files_listbox.insert(tk.END, i)
                programstate.save_data(self)

    def data_refresh(self):
        print("Обновление данных")
        self.generate_sample_data()
        self.clear_treeview()
        self.populate_treeview()

    def generate_sample_data(self):
        self.data = []
        departments = ["HR", "IT", "Finance", "Marketing", "Operations", "Sales", "R&D"]
        positions = ["Intern", "Junior", "Associate", "Senior", "Lead", "Manager", "Director"]
        statuses = ["Active", "On Leave", "Contract", "Remote", "Probation"]
        performance_ratings = ["Excellent", "Good", "Average", "Fair", "Poor"]
        
        # Generate random start dates within the last 10 years
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3650)  # ~10 years
        
        for i in range(100):
            # Generate a random email based on a random name
            first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 8))).capitalize()
            last_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 10))).capitalize()
            email = f"{first_name.lower()}.{last_name.lower()}@company.com"
            
            # Generate random date string
            random_days = random.randint(0, (end_date - start_date).days)
            random_date = start_date + timedelta(days=random_days)
            date_str = random_date.strftime("%Y-%m-%d")
            
            # Create the data row
            row = {
                "id": i + 1,
                "name": f"{first_name} {last_name}",
                "department": random.choice(departments),
                "position": random.choice(positions),
                "age": random.randint(22, 65),
                "salary": random.randint(30000, 150000),
                "start_date": date_str,
                "performance": random.choice(performance_ratings),
                "projects": random.randint(0, 15),
                "email": email,
                "status": random.choice(statuses)
            }
            self.data.append(row)
    
    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def populate_treeview(self):

        for item in self.data:
            values = (
                item["name"],
                item["department"],
                item["position"],
                item["age"],
                item["salary"],
                item["start_date"],
                item["performance"],
                item["projects"],
                item["email"],
                item["status"]
            )
            self.tree.insert("", tk.END, text=str(item["id"]), values=values)

    
    def sort_treeview_column(self, col):
        """Sort the treeview based on the clicked column"""
        # Adjust for the ID column which is #0
        tree_col = col
        data_col = col - 1  # Data columns are 0-based, treeview columns are 1-based
        
        # Determine data type for proper sorting
        if col == 4:  # Age column
            key_func = lambda x: int(x[data_col]) if x[data_col].isdigit() else 0
        elif col == 5:  # Salary column
            key_func = lambda x: int(x[data_col]) if x[data_col].isdigit() else 0
        elif col == 8:  # Projects column
            key_func = lambda x: int(x[data_col]) if x[data_col].isdigit() else 0
        else:
            key_func = lambda x: x[data_col].lower()
        # If already sorting by this column, reverse the order
        if self.sort_column == tree_col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = tree_col
            self.sort_reverse = False
        
        # Get all items
        item_list = [(self.tree.item(item, "text"), self.tree.item(item, "values")) 
                    for item in self.tree.get_children("")]
        
        # Sort the list
        item_list.sort(key=lambda x: key_func(x[1]), reverse=self.sort_reverse)
        
        # Clear and repopulate in sorted order
        for item in self.tree.get_children(""):
            self.tree.delete(item)
            
        for item_id, values in item_list:
            self.tree.insert("", tk.END, text=item_id, values=values)
            
        # Update the heading to show sort direction
        for i in range(1, 11):
            if i == col:
                direction = " ↓" if self.sort_reverse else " ↑"
                column_names = ["Name", "Department", "Position", "Age", "Salary", 
                               "Start Date", "Performance", "Projects", "Email", "Status"]
                self.tree.heading(i, text=f"{column_names[i-1]}{direction}")
            else:
                column_names = ["Name", "Department", "Position", "Age", "Salary", 
                               "Start Date", "Performance", "Projects", "Email", "Status"]
                self.tree.heading(i, text=column_names[i-1])

def main():
    print(os.getenv('LOCALAPPDATA'))
    root = tk.Tk()
    root.title("Обработчик журналов IIS")
    root.geometry("1200x800")
    root.default_font = tkFont.nametofont("TkDefaultFont")
    #root.default_font.configure(size=10)
    app = SortableDataGrid(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
