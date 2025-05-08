PROGRAM_NAME = "Fast Log Viewer"
ROW_LIMIT = 10000 # ограничение количества строк датагрида. Только отображение, в экспорт идёт вся выборка
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SHOW_LIMIT = 10000
DELIMITERS = [" ", ","]
DEFAULT_DELIMITER = " "
LOG_TYPES = ("IIS Log", "Exchange Log", "Proxy", "CSV")
DEFAULT_LOG_TYPE = "IIS Log"
DEFAULT_TIMEZONE = 3
DATATAB_LABEL = "Данные"
FILESTAB_LABEL = "Выбор журналов"
SELECTED_LOGS = "Выбранные журналы:" 
LOG_TYPE = "Тип журналов:"
DELIMITER_CSV = "Разделитель CSV:" 
TIMEZONE_CORRECTION = "Коррекция таймзоны:"
WRONG_TIMEZONE ="Формат: целое число от -23 до (+)23"
WRONG_TIMEZONE_HEADER = "Неправильный формат таймзоны"

# Константы для сплеш-скрина
SPLASH_WIDTH = 580
SPLASH_HEIGHT = 387
SPLASH_BG_COLOR = 'pink'
SPLASH_DISPLAY_TIME = 2000  # время отображения сплеш-скрина в миллисекундах

# Константы для файлового диалога
FILE_DIALOG_TITLE = "Выбор журналов"
FILE_DIALOG_TYPES = (
    ("Все файлы", "*.*"),
    ("Журналы", "*.log"),
)

# Константы для сохранения файлов
SAVE_DIALOG_TITLE = "Сохранение файла"
SAVE_DIALOG_DEFAULT_NAME = "Untitled.csv"
SAVE_DIALOG_TYPES = [
    ("Все файлы", "*.*"),
    ("Документы CSV", "*.csv")
]

HELP_TEXT = """Порядок: 
На вкладке "Выбор журналов":
1. Выбрать журналы.
2. Выбрать тип журналов, разделитель (только для CSV), коррекцию таймзоны в часах (кроме CSV).

На вкладке "Данные":
1. Нажать кнопку "Загрузить журналы". Эту кнопку нужно нажимать после изменения списка журналов, типа журналов и тд на вкладке "Выбор журналов".
Фактически формирует набор данных, с которым потом работают SQL-запросы.
2. Отредактировать SQL, нажать кнопку "Запустить запрос".
3. Для сохранения результатов нажать "Экспорт в CSV".
"""

DEFAULT_SQL = """# Документация по синтаксису SQL: https://docs.pola.rs/api/python/stable/reference/sql/index.html
# Для журналов, в которых определены названия колонок, символы "-" и "(" в названиях полей заменяются на "_", символ ")" удаляется
# Пример для IIS: SELECT cs_username, count(sc_status) FROM LogData WHERE sc_status = 200 GROUP BY cs_username
# Пример для Exchange: SELECT date_time, message_id AS ID FROM LogData WHERE date_time > '2025-04-22 09:00:04' AND date_time < '2025-04-22 09:10:00' 
# Количество возвращаемых полей влияет на скорость работы. Иногда разница в разы. Выбирайте нужные поля вместо "*"

SELECT * FROM LogData LIMIT 100 /*количество выводимых строк ограничено для ускорения начальной загрузки*/
"""

DEFAULT_SQL_IIS = """
SELECT  * FROM LogData LIMIT 100
"""
