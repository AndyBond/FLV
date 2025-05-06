import tkinter as tk
from tkinter import ttk

class ResizableWidgetsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resizable Widgets Demo")
        self.root.geometry("800x600")
        
        # Создаем главный фрейм, который займет все пространство окна
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Устанавливаем минимальный размер окна
        root.minsize(400, 300)
        
        # Создаем TreeView в верхней части окна
        self.tree_frame = tk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем TreeView с колонками для демонстрации
        self.tree = ttk.Treeview(self.tree_frame, columns=("Column 1", "Column 2", "Column 3"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Column 1", text="Name")
        self.tree.heading("Column 2", text="Email")
        self.tree.heading("Column 3", text="Status")
        
        # Добавляем прокрутки для TreeView
        tree_vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        tree_hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_vsb.set, xscrollcommand=tree_hsb.set)
        
        # Размещаем элементы TreeView
        tree_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Заполняем TreeView тестовыми данными
        for i in range(20):
            self.tree.insert("", tk.END, text=str(i), 
                            values=(f"User {i}", f"user{i}@example.com", "Active" if i % 2 == 0 else "Inactive"))
        
        # Создаем разделитель (sash), который можно будет перетаскивать
        self.sash = tk.Frame(self.main_frame, height=5, bg="gray", cursor="sizing")
        self.sash.pack(fill=tk.X)
        
        # Создаем Text widget в нижней части окна
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text = tk.Text(self.text_frame)
        
        # Добавляем прокрутки для Text
        text_vsb = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.text.yview)
        text_hsb = ttk.Scrollbar(self.text_frame, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=text_vsb.set, xscrollcommand=text_hsb.set, wrap="none")
        
        # Размещаем элементы Text
        text_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        text_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Добавляем тестовый текст
        self.text.insert(tk.END, "Это текстовый виджет.\n\n"
                        "Вы можете изменить размер этого виджета и TreeView выше, "
                        "перетаскивая серую полосу между ними.\n\n"
                        "Попробуйте нажать и перетащить полосу вверх или вниз.")
        
        # Переменные для отслеживания изменения размера
        self.dragging = False
        self.start_y = 0
        self.start_height = 0
        
        # Привязываем события мыши к разделителю
        self.sash.bind("<ButtonPress-1>", self.start_resize)
        self.sash.bind("<B1-Motion>", self.do_resize)
        self.sash.bind("<ButtonRelease-1>", self.stop_resize)
        
        # Начальное соотношение размеров - по умолчанию 50/50
        self.root.update()
        total_height = self.main_frame.winfo_height()
        self.tree_frame.configure(height=total_height/2)
        self.text_frame.configure(height=total_height/2)
    
    def start_resize(self, event):
        """Начало изменения размера при нажатии кнопки мыши"""
        self.dragging = True
        self.start_y = event.y_root
        self.start_tree_height = self.tree_frame.winfo_height()
        self.start_text_height = self.text_frame.winfo_height()
    
    def do_resize(self, event):
        """Изменение размера при перемещении мыши"""
        if not self.dragging:
            return
            
        # Вычисляем смещение
        delta_y = event.y_root - self.start_y
        
        # Получаем текущую высоту виджетов и окна
        total_height = self.main_frame.winfo_height() - self.sash.winfo_height()
        new_tree_height = self.start_tree_height + delta_y
        new_text_height = self.start_text_height - delta_y
        
        # Проверяем минимальные допустимые размеры (не менее 50 пикселей для каждого виджета)
        min_height = 50
        if new_tree_height < min_height or new_text_height < min_height:
            return
            
        # Устанавливаем новые размеры
        self.tree_frame.pack_forget()
        self.text_frame.pack_forget()
        
        self.tree_frame.configure(height=new_tree_height)
        self.text_frame.configure(height=new_text_height)
        
        # Пересобираем виджеты
        self.tree_frame.pack(before=self.sash, fill=tk.BOTH)
        self.text_frame.pack(after=self.sash, fill=tk.BOTH)
    
    def stop_resize(self, event):
        """Окончание изменения размера при отпускании кнопки мыши"""
        self.dragging = False

if __name__ == "__main__":
    root = tk.Tk()
    app = ResizableWidgetsApp(root)
    root.mainloop()