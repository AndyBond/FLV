import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import config
import programstate

class FileManager:
    def __init__(self, parent):
        self.parent = parent
        self.filelist = []
        self.files_listbox = None

    def setup_listbox(self, listbox):
        """Инициализация Listbox для отображения файлов"""
        self.files_listbox = listbox
        self.files_listbox.delete(0, tk.END)
        for sf in self.filelist:
            self.files_listbox.insert(tk.END, sf)
    # Вызов окна диалога выбора файлов и добавление выбранного в список с исключением дубликатов
    def select_files(self):
        """Выбор файлов через диалоговое окно"""
        filepaths = filedialog.askopenfilenames(
            title=config.FILE_DIALOG_TITLE,
            filetypes=config.FILE_DIALOG_TYPES
        )
        if filepaths:
            # Создаем set для исключения дубликатов
            temp_list = set(self.filelist)
            for filepath in filepaths:
                temp_list.add(filepath)
            
            self.filelist = list(temp_list)
            self.update_listbox()
            programstate.save_data(self.parent)
            return True
        return False

    def clear_files(self):
        """Удаление всех файлов из списка"""
        self.files_listbox.delete(0, tk.END)
        self.filelist.clear()
        programstate.save_data(self.parent)
    # удаление выбранных файлов из списка журналов
    def clear_selected_files(self):
        """Удаление выбранных файлов из списка"""
        ListToDelete = self.files_listbox.curselection()
        for item in reversed(ListToDelete):
            self.files_listbox.delete(item)
        
        self.filelist.clear()
        for i in self.files_listbox.get(0, self.files_listbox.size()):
            self.filelist.append(i)
        programstate.save_data(self.parent)
    # сохранение результата выборки в файл
    def save_csv(self):
        """Сохранение данных в CSV файл"""
        if not hasattr(self.parent, 'df'):
            messagebox.showerror("Ошибка", "Нет данных для сохранения")
            return False
        f = filedialog.asksaveasfilename(
            initialfile=config.SAVE_DIALOG_DEFAULT_NAME,
            defaultextension=".csv",
            filetypes=config.SAVE_DIALOG_TYPES
        )
        if len(f) > 1:
            f = f.replace("/", "\\")
            try:
                self.parent.df.write_csv(f)
                return True
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не получилось сохранить файл: {str(e)}")
        return False

    def update_listbox(self):
        """Обновление содержимого Listbox"""
        if self.files_listbox:
            self.files_listbox.delete(0, tk.END)
            for file in self.filelist:
                self.files_listbox.insert(tk.END, file)

    def get_filelist(self):
        """Получение списка файлов"""
        return self.filelist

    def set_filelist(self, filelist):
        """Установка списка файлов"""
        self.filelist = filelist
        self.update_listbox() 