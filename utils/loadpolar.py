import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import polars as pl
import os
from datetime import datetime

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer с Polars")
        self.root.geometry("800x600")
        
        # Создаем фрейм для элементов управления
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.pack(fill=tk.X)
        
        # Кнопка загрузки файла
        self.load_button = ttk.Button(self.control_frame, text="Загрузить CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Метка для отображения имени загруженного файла
        self.file_label = ttk.Label(self.control_frame, text="Файл не загружен")
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        # Создаем фрейм для таблицы
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Создаем скроллбары
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal")
        
        # Создаем Treeview (таблицу)
        self.tree = ttk.Treeview(self.tree_frame, columns=(), 
                                 show='headings',
                                 yscrollcommand=self.vsb.set,
                                 xscrollcommand=self.hsb.set)
        
        # Настраиваем скроллбары
        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)
        
        # Размещаем элементы в сетке
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        # Переменная для хранения DataFrame
        self.df = None
        
    def load_csv(self):
        """Загружает CSV файл и обрабатывает его с помощью Polars"""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        
        if not file_path:
            return
        
        try:
            # Получаем имя файла для отображения
            file_name = os.path.basename(file_path)
            self.file_label.config(text=f"Загружен: {file_name}")
            
            # Загружаем данные с автоматическим определением типов
            self.df = pl.read_csv(file_path, infer_schema_length=10000)
            
            # Преобразуем колонки типа Date в нужный формат
            for col in self.df.columns:
                if self.df[col].dtype == pl.Datetime:
                    # В Polars уже корректный тип данных для datetime
                    pass
            
            # Отображаем данные в таблице
            self.display_data()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def display_data(self):
        """Отображает Polars DataFrame в Treeview"""
        # Очищаем существующую таблицу
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Настраиваем колонки
        self.tree['columns'] = self.df.columns
        
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Стандартная ширина
            
        # Добавляем строки
        for idx, row in enumerate(self.df.iter_rows()):
            # Преобразуем значения в строки для отображения
            values = []
            for value in row:
                if isinstance(value, datetime):
                    values.append(value.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    values.append(str(value))
            
            self.tree.insert('', tk.END, iid=str(idx), values=values)

def main():
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
