PROGRAM_NAME = "Fast Log Viewer"
ROW_LIMIT = 10000 # ограничение количества строк датагрида. Только отображение, в экспорт идёт вся выборка
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SHOW_LIMIT = 10000
DELIMITERS = [" ", ","]
DEFAULT_DELIMITER = " "
LOG_TYPES = ("IIS Log", "Exchange Log", "Proxy", "CSV")
DEFAULT_LOG_TYPE = "IIS Log"
DATATAB_LABEL = "Данные"
FILESTAB_LABEL = "Выбор журналов"
SELECTED_LOGS = "Выбранные журналы:" 
DEFAULT_SQL = """
# Это дефолтный запрос.
# Документация по синтаксису SQL: https://docs.pola.rs/api/python/stable/reference/sql/index.html
# Для журналов, в которых определены названия колонок, символы "-" и "(" в названиях полей заменяются на "_", символ ")" удаляется
# Пример для IIS: SELECT cs_username, count(sc_status) FROM LogData WHERE sc_status = 200 GROUP BY cs_username

SELECT * FROM LogData LIMIT 100 /*количество выводимых строк ограничено для ускорения начальной загрузки*/
"""
DEFAULT_SQL_IIS = """
SELECT  * FROM LogData LIMIT 100
"""
