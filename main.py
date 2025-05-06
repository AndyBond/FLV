from time import time

from lib.analyzer import Analyzer
from lib.helpers import Helpers
#from lib.writer import Writer
import sqlite3
import sqltest

ENCODING = "utf8"
FILEFORMAT = ".log"
#DB = sqlite3.connect("file::memory:?cache=shared", uri=True)
DB = sqlite3.connect("my.db")

if __name__ == '__main__':
    print("Running Log Auswertung")
    start = time()

    helpers = Helpers(ENCODING, FILEFORMAT)
    helpers.create_directorys()
    #helpers.create_table(DB)
    
    #helpers.load_db(DB)
    end = time() - start
    print("Загрузка: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
    request_start = time()
    helpers.show_table(DB)
    #analyzer = Analyzer(helpers)
    #analyzer.run()
    end = time() - request_start
    print("Запрос: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
