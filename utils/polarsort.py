import tkinter as tk
from tkinter import ttk, filedialog
import polars as pl
from datetime import datetime

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Viewer")
        self.root.geometry("800x600")
        
        # Создаем фрейм для кнопок
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Кнопка для загрузки CSV файла
        self.load_button = tk.Button(self.button_frame, text="Загрузить CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Создаем фрейм для таблицы с полосой прокрутки
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем Treeview для отображения данных
        self.tree = ttk.Treeview(self.table_frame)
        
        # Добавляем вертикальную полосу прокрутки
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Добавляем горизонтальную полосу прокрутки
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=hsb.set)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Переменная для хранения DataFrame
        self.df = None
        
        # Переменная для отслеживания направления сортировки
        self.sort_direction = {}
        
    def load_csv(self):
        # Открываем диалог выбора файла
        filepath = filedialog.askopenfilename(
            title="Выберите CSV файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                # Загружаем CSV в Polars DataFrame
                self.df = pl.read_csv(filepath)
                
                # Отображаем данные в таблице
                self.display_data()
                
                # Инициализируем словарь направлений сортировки
                self.sort_direction = {col: False for col in self.df.columns}
                
            except Exception as e:
                tk.messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def display_data(self):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Настраиваем столбцы
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"  # Скрываем первую колонку с id
        
        # Определяем заголовки столбцов
        for column in self.df.columns:
            self.tree.heading(column, text=column, command=lambda col=column: self.sort_by_column(col))
            # Устанавливаем ширину столбца в зависимости от типа данных
            col_type = str(self.df[column].dtype)
            if "Int" in col_type:
                width = 100
            elif "Datetime" in col_type:
                width = 150
            else:
                width = 200
            self.tree.column(column, width=width, minwidth=50)
        
        # Заполняем таблицу данными
        for i, row in enumerate(self.df.iter_rows(named=True)):
            values = [str(row[col]) for col in self.df.columns]
            self.tree.insert("", tk.END, text=str(i), values=values)
    
    def sort_by_column(self, column):
        if self.df is not None:
            # Меняем направление сортировки при повторном клике
            self.sort_direction[column] = not self.sort_direction[column]
            ascending = self.sort_direction[column]
            
            # Сортируем DataFrame
            sorted_df = self.df.sort(column, descending=not ascending)
            self.df = sorted_df
            
            # Обновляем отображение
            self.display_data()
            
            # Визуальный индикатор направления сортировки
            if ascending:
                sort_indicator = "▲"
            else:
                sort_indicator = "▼"
            
            # Обновляем заголовок, чтобы показать направление сортировки
            for col in self.df.columns:
                if col == column:
                    self.tree.heading(col, text=f"{col} {sort_indicator}")
                else:
                    self.tree.heading(col, text=col)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()