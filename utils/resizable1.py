import tkinter as tk
from tkinter import ttk
import time


class ResizableWidgetsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resizable Treeview and Text")
        self.root.geometry("800x600")
        
        # Создаем основной контейнер
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем верхний фрейм для Treeview
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        self.top_frame.pack_propagate(0)
        
        # Создаем Treeview
        self.tree = ttk.Treeview(self.top_frame, columns=("Column 1", "Column 2", "Column 3"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Column 1", text="Название")
        self.tree.heading("Column 2", text="Описание")
        self.tree.heading("Column 3", text="Значение")
        
        # Настраиваем ширину столбцов
        self.tree.column("#0", width=50, minwidth=50)
        self.tree.column("Column 1", width=150, minwidth=100)
        self.tree.column("Column 2", width=250, minwidth=150)
        self.tree.column("Column 3", width=100, minwidth=80)
        
        # Добавляем полосы прокрутки для Treeview
        tree_scroll_y = ttk.Scrollbar(self.top_frame, orient="vertical", command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(self.top_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        # Размещаем Treeview и полосы прокрутки
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Заполняем Treeview примерными данными
        for i in range(20):
            self.tree.insert("", tk.END, text=f"{i+1}", values=(f"Элемент {i+1}", f"Описание элемента {i+1}", f"{i*10}"))
        
        # Создаем разделитель (sash)
        self.sash = tk.Frame(self.main_frame, height=5, bg="gray", cursor="sb_v_double_arrow")
        self.sash.pack(fill=tk.X)
        
        # Создаем нижний фрейм для Text виджета
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)
        self.bottom_frame.pack_propagate(0)
        
        # Создаем Text виджет
        self.text = tk.Text(self.bottom_frame, wrap=tk.WORD)
        self.text.insert(tk.END, "Это текстовый виджет. Вы можете изменить размер между Treeview и этим виджетом, перетаскивая серую полосу разделителя.\n\n" * 10)
        
        # Добавляем полосы прокрутки для Text
        text_scroll_y = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.text.yview)
        text_scroll_x = ttk.Scrollbar(self.bottom_frame, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=text_scroll_y.set, xscrollcommand=text_scroll_x.set)
        
        # Размещаем Text и полосы прокрутки
        text_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Настройка начальных размеров (50% - 50%)
        self.root.update()
        self.total_height = self.main_frame.winfo_height()
        self.top_frame.configure(height=self.total_height/2)
        self.bottom_frame.configure(height=self.total_height/2)
        
        # Переменные для обработки перемещения разделителя
        self.dragging = False
        self.start_y = 0
        self.start_top_height = 0
        self.start_bottom_height = 0
        
        # Привязка событий к разделителю
        self.sash.bind("<ButtonPress-1>", self.on_sash_press)
        self.sash.bind("<B1-Motion>", self.on_sash_motion)
        self.sash.bind("<ButtonRelease-1>", self.on_sash_release)
        
        # Обработка изменения размера окна
        self.root.bind("<Configure>", self.on_window_resize)

        """
        time.sleep(5.5)    # Pause 5.5 seconds
        print("something")
        self.top_frame.pack_forget()
        self.top_frame.configure(height=self.total_height/3)
        self.bottom_frame.configure(height=self.total_height/3*2)
        self.root.update()
        """
    def on_sash_press(self, event):
        # Запоминаем начальное положение и размеры при нажатии кнопки мыши
        self.dragging = True
        self.start_y = event.y_root
        self.start_top_height = self.top_frame.winfo_height()
        self.start_bottom_height = self.bottom_frame.winfo_height()
    
    def on_sash_motion(self, event):
        # Вычисляем новые размеры при перемещении разделителя
        if self.dragging:
            delta_y = event.y_root - self.start_y
            new_top_height = max(50, self.start_top_height + delta_y)
            new_bottom_height = max(50, self.start_bottom_height - delta_y)
            
            # Получаем общую высоту области контента
            total_height = self.main_frame.winfo_height() - self.sash.winfo_height()
            
            # Проверяем, чтобы не выходило за пределы
            if new_top_height + new_bottom_height <= total_height:
                # Применяем новые размеры
                self.top_frame.pack_forget()
                self.sash.pack_forget()
                self.bottom_frame.pack_forget()
                
                self.top_frame.configure(height=new_top_height)
                self.bottom_frame.configure(height=new_bottom_height)
                
                self.top_frame.pack(fill=tk.BOTH, expand=False)
                self.sash.pack(fill=tk.X)
                self.bottom_frame.pack(fill=tk.BOTH, expand=False)
    
    def on_sash_release(self, event):
        # Завершаем перетаскивание при отпускании кнопки мыши
        self.dragging = False
        
        # Обновляем размеры окна для фиксации новых значений
        self.top_frame.pack(fill=tk.BOTH, expand=True)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)
    
    def on_window_resize(self, event):
        # Обработка изменения размера основного окна
        if event.widget == self.root:
            # Пересчитываем пропорции при изменении размера окна
            self.root.update_idletasks()
            
            # Пропускаем первоначальную настройку
            if hasattr(self, 'last_height') and self.last_height > 0:
                ratio = self.root.winfo_height() / self.last_height
                
                # Обновляем размеры с сохранением пропорций
                top_height = int(self.top_frame.winfo_height() * ratio)
                bottom_height = int(self.bottom_frame.winfo_height() * ratio)
                
                # Применяем новые размеры
                self.top_frame.configure(height=top_height)
                self.bottom_frame.configure(height=bottom_height)
            
            # Запоминаем текущую высоту для следующего пересчета
            self.last_height = self.root.winfo_height()

def SaveCSV(self):
    self.df.write_csv("f:\\output.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResizableWidgetsApp(root)
    root.mainloop()