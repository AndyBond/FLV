# Модуль для сохранения состояния и его загрузки  при старте программы
import json, os
from tkinter import messagebox
import tkinter as tk

def init_file(dataclass):
        # Создаем папку в локальной юзеровской appdata и файл конфига для сохранения настроек между запусками
        appdata_path = os.path.join(os.getenv('LOCALAPPDATA') or os.path.expanduser('~/.config'), 'FLV')
        os.makedirs(appdata_path, exist_ok=True)
        dataclass.json_path = os.path.join(appdata_path, 'flvconfig.json')

def LoadState(dataclass):
    # Load data from JSON file if it exists
    try:
        if os.path.exists(dataclass.json_path):
            with open(dataclass.json_path, 'r') as file:
                data = json.load(file)
            
            # Select items in listbox
            dataclass.file_manager.set_filelist(data.get("logs_list", []))
            dataclass.LogType = data.get("LogType")
            dataclass.Delimiter = data.get("Delimiter")
            if data.get("Timezone") is not None:
                dataclass.Timezone = data.get("Timezone")
    except Exception as e:
        messagebox.showerror("Ошибка загрузки", f"Не получилось загрузить сохраненные данные  {str(e)}")

def save_data(dataclass):
    #text_data = self.text_input.get()
    LogType = dataclass.LogType
    selected_items = dataclass.file_manager.get_filelist()
    Delimiter = dataclass.Delimiter
    Timezone = dataclass.Timezone

    data = {
        "LogType": LogType,
        "logs_list": selected_items,
        "Delimiter": Delimiter,
        "Timezone": Timezone
    }
    try:
        with open(dataclass.json_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не получилось сохранить данные  {str(e)}")