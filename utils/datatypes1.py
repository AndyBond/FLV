import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime, timedelta

# Генерация случайных данных
def generate_data(num_rows):
    data = []
    for _ in range(num_rows):
        row = {
            'int_column': random.randint(1, 100),
            'float_column': round(random.uniform(1.0, 100.0), 2),
            'str_column': random.choice(['apple', 'banana', 'cherry', 'date', 'elderberry']),
            'datetime_column': datetime.now() - timedelta(days=random.randint(0, 365)),
            'int_column2': random.randint(1, 100),
            'float_column2': round(random.uniform(1.0, 100.0), 2),
            'str_column2': random.choice(['alpha', 'beta', 'gamma', 'delta']),
            'datetime_column2': datetime.now() - timedelta(days=random.randint(0, 365)),
            'int_column3': random.randint(1, 100),
            'float_column3': round(random.uniform(1.0, 100.0), 2),
        }
        data.append(row)
    return data

# Типы данных для колонок
columns_data = {
    'int_column': int,
    'float_column': float,
    'str_column': str,
    'datetime_column': datetime,
    'int_column2': int,
    'float_column2': float,
    'str_column2': str,
    'datetime_column2': datetime,
    'int_column3': int,
    'float_column3': float
}

# Основное окно программы
root = tk.Tk()
root.title('DataGrid with Sorting')

# Функция сортировки
def sort_column(event, col_name):
    current_sort = sort_direction.get(col_name, 'ascending')
    if current_sort == 'ascending':
        sorted_data = sorted(data, key=lambda x: x[col_name], reverse=True)
        sort_direction[col_name] = 'descending'
    else:
        sorted_data = sorted(data, key=lambda x: x[col_name])
        sort_direction[col_name] = 'ascending'
    
    # Обновляем отображение в таблице
    for i, row in enumerate(sorted_data):
        for j, col in enumerate(columns_data.keys()):
            treeview.set(treeview.get_children()[i], column=col, value=row[col])
    
    data[:] = sorted_data

# Сортировка по умолчанию
sort_direction = {}

# Генерация данных
data = generate_data(100)

# Верхняя панель с иконками
frame_icons = tk.Frame(root)
frame_icons.pack(side='top', fill='x', pady=5)

# Добавляем три иконки в верхнюю панель
icon1 = tk.Label(frame_icons, text='Icon1', relief='solid', width=10, height=2)
icon1.grid(row=0, column=0, padx=5)
icon2 = tk.Label(frame_icons, text='Icon2', relief='solid', width=10, height=2)
icon2.grid(row=0, column=1, padx=5)
icon3 = tk.Label(frame_icons, text='Icon3', relief='solid', width=10, height=2)
icon3.grid(row=0, column=2, padx=5)

# Нижняя панель с DataGrid
frame_grid = tk.Frame(root)
frame_grid.pack(side='bottom', fill='both', expand=True)

# Создаем DataGrid (treeview)
vsb = ttk.Scrollbar(frame_grid, orient=tk.VERTICAL)
hsb = ttk.Scrollbar(frame_grid, orient=tk.HORIZONTAL)
treeview = ttk.Treeview(frame_grid, columns=list(columns_data.keys()), show="headings", height=20, selectmode="extended", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
treeview.pack(fill='both', expand=True)

# Настройка заголовков
for col in columns_data.keys():
    treeview.heading(col, text=col, command=lambda col=col: sort_column(None, col))
    treeview.column(col, width=100)

# Вставляем данные в DataGrid
for row in data:
    treeview.insert('', 'end', values=[row[col] for col in columns_data.keys()])

# Запуск программы
root.mainloop()