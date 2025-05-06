# Функции для чтения логов разных форматов
# берет список файлов, открывает первый и пытается считать заголовки    (IIS, Exchange)
from tkinter import messagebox
import polars
from datetime import datetime, timedelta
import config



def GetHeaders(app, delimiter):
    # Читает первые строки, до 10-й, и если находит в них подстроку "#Fields", использует ее как источник колонок
    # В IIS в именах полей есть "-", polars считает его математическим знаком. Поэтому, меняем его на подчеркивание. То же самое со скобками.
    i = 0
    FirstLog = app.filelist[0]
    with open(FirstLog, 'r', encoding='utf8', errors='ignore') as lines:
        for l in lines:
            if l[:8] == "#Fields:":
                hl = l[9:-1]
                hl = hl.replace("-","_").replace("(","_").replace(")","")
                Headers = hl.split(delimiter)
                app.column_names.clear()
                for h in Headers:
                    app.column_names.append(h)
                return
            i += 1
            if i >= 10:
                return


def DELETEmake_date(strdate, strtime):
    """
    Функция берет текстовые поля дата и время из лога и делает из них одно поле формата "дата", добавляя 3 часа
    """
    newdate = datetime.strptime(strdate + " " + strtime, '%Y-%m-%d %H:%M:%S')
    newdate = newdate + timedelta(hours=3)
    return(newdate)

def LoadDataIIS(app):
    delimiter = " "
    GetHeaders(app, delimiter)
    tempSQLArray = config.DEFAULT_SQL_IIS.split("\n")
    tempSQLArray = app.filter_non_comment_lines(tempSQLArray)
    RequestSQL = ' '.join(tempSQLArray).strip()
    try:
        # Загружаем данные с автоматическим определением типов
        app.LogData = polars.scan_csv(app.filelist, comment_prefix="#",has_header=False, separator=delimiter, encoding="utf8", quote_char= None, new_columns=app.column_names).with_columns(date_column = polars.concat_str(polars.col("date"), polars.col("time")).str.strptime(polars.Datetime, '%Y-%m-%d %H:%M:%S').dt.offset_by("3h")).drop('time').drop('date')
        app.ctx = polars.SQLContext(LogData=app.LogData, eager=True)
        app.df = app.ctx.execute(RequestSQL)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файлы журналов: {str(e)}")

def LoadDataExchange(app):
    delimiter = ","
    GetHeaders(app, delimiter)
    tempSQLArray = config.DEFAULT_SQL.split("\n")
    tempSQLArray = app.filter_non_comment_lines(tempSQLArray)
    RequestSQL = ' '.join(tempSQLArray).strip()
    try:
        # Загружаем данные с автоматическим определением типов
        app.LogData = polars.scan_csv(app.filelist, comment_prefix="#",has_header=False, separator=delimiter, encoding="utf8", new_columns=app.column_names)
        app.ctx = polars.SQLContext(LogData=app.LogData, eager=True)
        app.df = app.ctx.execute(RequestSQL)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файлы журналов: {str(e)}")

def LoadDataProxy(app):
    delimiter = chr(1) # фейковый разделитель, такого символа не должно быть в строке. Читерство.
    # это фиксированная строка, чтобы можно было доставать выделенные поля по индексу.
    pattern = r'([\d.]+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) (<[^>]*>) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+)'

    tempSQLArray = config.DEFAULT_SQL.split("\n")
    tempSQLArray = app.filter_non_comment_lines(tempSQLArray)
    RequestSQL = ' '.join(tempSQLArray).strip()
    try:
        # временный датафрейм, каждая строка = 1 колонка
        raw_df = polars.scan_csv(app.filelist,  comment_prefix="#",has_header=False, separator=delimiter, encoding="utf8", eol_char="\n")
        app.LogData = raw_df.with_columns([
            polars.col('column_1').str.extract(pattern, 1).cast(polars.Float64).alias("c1"),
            polars.col('column_1').str.extract(pattern, 2).alias("c2"),
            polars.col('column_1').str.extract(pattern, 3).alias("c3"),
            polars.col('column_1').str.extract(pattern, 4).alias("c4"),
            polars.col('column_1').str.extract(pattern, 5).alias("c5"),
            polars.col('column_1').str.extract(pattern, 6).alias("c6"),
            polars.col('column_1').str.extract(pattern, 7).alias("c7"),
            polars.col('column_1').str.extract(pattern, 8).alias("c8"),
            polars.col('column_1').str.extract(pattern, 9).alias("c9"),
            polars.col('column_1').str.extract(pattern, 10).alias("c10"),
            polars.col('column_1').str.extract(pattern, 11).alias("c11"),
            polars.col('column_1').str.extract(pattern, 12).alias("c12"),
            polars.col('column_1').str.extract(pattern, 13).alias("c13"),
            polars.col('column_1').str.extract(pattern, 14).alias("c14"),
            polars.col('column_1').str.extract(pattern, 15).alias("c15"),
            polars.col('column_1').str.extract(pattern, 16).alias("c16"),
            polars.col('column_1').str.extract(pattern, 17).alias("c17"),
            polars.col('column_1').str.extract(pattern, 18).alias("c18")
        ]).with_columns(polars.from_epoch("c1", time_unit="s").dt.offset_by("3h")).drop('column_1').lazy()

        app.ctx = polars.SQLContext(LogData=app.LogData, eager=True)
        app.df = app.ctx.execute(RequestSQL)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файлы журналов: {str(e)}")

def LoadDataCSV(app):
    delimiter = app.Delimiter
    tempSQLArray = config.DEFAULT_SQL.split("\n")
    tempSQLArray = app.filter_non_comment_lines(tempSQLArray)
    RequestSQL = ' '.join(tempSQLArray).strip()
    try:
        # Загружаем данные с автоматическим определением типов
        app.LogData = polars.scan_csv(app.filelist, comment_prefix="#",has_header=False, separator=delimiter, encoding="utf8")
        app.ctx = polars.SQLContext(LogData=app.LogData, eager=True)
        app.df = app.ctx.execute(RequestSQL)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файлы журналов: {str(e)}")

