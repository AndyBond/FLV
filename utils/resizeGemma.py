import tkinter as tk
from tkinter import ttk

class ResizableWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Resizable Window")

        # Инициализация размеров и позиций
        self.treeview_height = 200
        self.textwidget_height = 200
        self.total_height = self.treeview_height + self.textwidget_height
        self.width = 500

        # Создание Treeview
        self.tree = ttk.Treeview(root, height=self.treeview_height)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Создание Text widget
        self.text = tk.Text(root, height=self.textwidget_height)
        self.text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Разделитель (frame для перетаскивания)
        self.separator = tk.Frame(root, width=self.width, height=5, bg="gray")
        self.separator.pack(side=tk.TOP, fill=tk.X)  # Располагаем горизонтально

        # Привязка событий мыши к разделителю
        self.separator.bind("<ButtonPress-1>", self.start_resize)
        self.separator.bind("<B1-Motion>", self.resize)
        self.separator.bind("<ButtonRelease-1>", self.stop_resize)

        # Флаг, указывающий, идет ли перетаскивание
        self.resizing = False
        self.start_y = 0


    def start_resize(self, event):
        """Начало процесса изменения размера."""
        self.resizing = True
        self.start_y = event.y

    def resize(self, event):
        """Изменение размера Treeview и Text widget при перетаскивании разделителя."""
        if self.resizing:
            delta_y = event.y - self.start_y
            new_treeview_height = max(100, self.treeview_height + delta_y)  # Минимальная высота 100
            new_textwidget_height = max(100, self.textwidget_height - delta_y) # Минимальная высота 100

            self.treeview_height = new_treeview_height
            self.textwidget_height = new_textwidget_height
            self.total_height = self.treeview_height + self.textwidget_height

            # Изменение размеров виджетов
            self.tree.config(height=self.treeview_height)
            self.text.config(height=self.textwidget_height)

    def stop_resize(self, event):
        """Завершение процесса изменения размера."""
        self.resizing = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ResizableWindow(root)
    root.mainloop()
