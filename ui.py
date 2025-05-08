# Это будет модуль для всякий интерфейсных штучек
from tkinter import ttk
import tkinter as tk

# Таб данных
def SetupIconFrame(frame):
    frame.grid_icon_frame = tk.Frame(frame.tab_front, height=50)
    frame.grid_icon_frame.pack(fill=tk.X, padx=10, pady=10)
    frame.grid_icon_frame.pack_propagate(0)

def SetupDataFrame(frame):
    frame.tree_frame = tk.Frame(frame.tab_front)
    frame.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=0)
    frame.tree_frame.pack_propagate(0)

def SetupDividerFrame(frame):
    frame.divider_frame = tk.Frame(frame.tab_front, height=20, cursor="sb_v_double_arrow")
    frame.divider_frame.pack(fill=tk.X, padx=10, pady=0)
    frame.divider_frame.pack_propagate(0)
    # Привязка событий к разделителю
    frame.divider_frame.bind("<ButtonPress-1>", lambda event:on_divider_press(frame,event))
    frame.divider_frame.bind("<B1-Motion>", lambda event:on_divider_motion(frame, event))
    frame.divider_frame.bind("<ButtonRelease-1>", lambda event:on_divider_release(frame, event))   
    # всякая инфа
    frame.TimeLabel = ttk.Label(frame.divider_frame, text="Время загрузки: ")
    frame.TimeLabel.pack(side=tk.LEFT, padx=10)
    frame.NumberLabel = ttk.Label(frame.divider_frame, textvariable=frame.NumberLabelText) # количество записей результата
    frame.NumberLabel.pack(side=tk.LEFT, padx=10)     
    frame.RefreshLabel = ttk.Label(frame.divider_frame, textvariable=frame.RefreshLabelText) # время обработки запроса
    frame.RefreshLabel.pack(side=tk.LEFT, padx=10)
    frame.DividerLabel = ttk.Label(frame.divider_frame, text="|")
    frame.DividerLabel.pack(side=tk.LEFT, padx=0)   
    frame.TypeLabel = ttk.Label(frame.divider_frame, text=" Тип журнала: " + frame.LogType, font='Helvetica 9 bold')
    frame.TypeLabel.pack(side=tk.LEFT, padx=10)    

def SetupRequestFrame(frame):
    frame.request_frame = tk.Frame(frame.tab_front)
    frame.request_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    frame.request_frame.pack_propagate(0)   

def SetupDataGrid(frame):
    # ================================================================================================
    # грид пока без данных       
    # Создаем treeview, колонки не определяем, они зависят от данных, которых пока нет
    frame.tree = ttk.Treeview(frame.tree_frame,  show="headings", height=20, selectmode="extended")
    # Create scrollbars
    frame.vsb = ttk.Scrollbar(frame.tree_frame, orient=tk.VERTICAL, command=frame.tree.yview)
    frame.hsb = ttk.Scrollbar(frame.tree_frame, orient=tk.HORIZONTAL, command=frame.tree.xview)
    frame.tree.configure(yscrollcommand=frame.vsb.set, xscrollcommand=frame.hsb.set) # в treeview вставили скролбары

    # Размещаем Treeview и полосы прокрутки
    frame.vsb.pack(side=tk.RIGHT, fill=tk.Y)
    frame.hsb.pack(side=tk.BOTTOM, fill=tk.X)
    frame.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 

def SetupRequestEditor(frame):
        # Создаем Text виджет
        frame.text = tk.Text(frame.request_frame, wrap=tk.WORD)
        frame.text.insert(tk.END, frame.RequestSQL)
        
        # Добавляем полосы прокрутки для Text
        text_scroll_y = ttk.Scrollbar(frame.request_frame, orient="vertical", command=frame.text.yview)
        text_scroll_x = ttk.Scrollbar(frame.request_frame, orient="horizontal", command=frame.text.xview)
        frame.text.configure(yscrollcommand=text_scroll_y.set, xscrollcommand=text_scroll_x.set)
        
        # Размещаем Text и полосы прокрутки
        text_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        frame.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 

# Функции событий
def on_divider_press(topclass, event):
    # Запоминаем начальное положение и размеры при нажатии кнопки мыши
    topclass.dragging = True
    topclass.start_y = event.y_root
    topclass.start_top_height = topclass.tree_frame.winfo_height()
    topclass.start_bottom_height = topclass.request_frame.winfo_height()

def on_divider_motion(topclass, event):
    # Вычисляем новые размеры при перемещении разделителя
    if topclass.dragging:
        delta_y = event.y_root - topclass.start_y
        new_top_height = max(50, topclass.start_top_height + delta_y)
        new_bottom_height = max(50, topclass.start_bottom_height - delta_y)
        
        # Получаем общую высоту области контента
        total_height = topclass.tab_front.winfo_height() - topclass.divider_frame.winfo_height() - topclass.grid_icon_frame.winfo_height()
        # Проверяем, чтобы не выходило за пределы
        if new_top_height + new_bottom_height <= total_height:
            # Применяем новые размеры
            topclass.tree_frame.pack_forget()
            topclass.divider_frame.pack_forget()
            topclass.request_frame.pack_forget()
            
            topclass.tree_frame.configure(height=new_top_height)
            topclass.request_frame.configure(height=new_bottom_height)
            
            topclass.tree_frame.pack(fill=tk.BOTH, expand=False)
            topclass.divider_frame.pack(fill=tk.X)
            topclass.request_frame.pack(fill=tk.BOTH, expand=False)

def on_divider_release(topclass, event):
    # Завершаем перетаскивание при отпускании кнопки мыши
    topclass.dragging = False
    # Обновляем размеры окна для фиксации новых значений
    topclass.tree_frame.pack(fill=tk.BOTH, expand=True)
    topclass.request_frame.pack(fill=tk.BOTH, expand=True)   