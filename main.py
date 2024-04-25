import datetime

import AppLogic.App
import DatabaseMethods.DatabaseMethodsImpl
import ArticlesMethods.SelectPdfFilesLocal
import ArticlesMethods.GetRawTextFromURL
from GigaChainMethods import GigaChainMethodsImpl

if __name__ == '__main__':
    conn_string = "dbname=sber-hack-database user=admin password=admin host=localhost port=2432"
    database = DatabaseMethods.DatabaseMethodsImpl.DatabaseMethods(conn_string)
    gigachat_methods = GigaChainMethodsImpl.GigaChainMethodsImpl("NTlkY2MyZmItM2Q4ZC00ZWMzLWE2NjAtNTI3MzZhOTk2ZjQzOjVhZGJiZDQxLTc0YjAtNDQxNi04YjAzLTUxZDVmYTY4NTkwNw==")
    raw_text = ArticlesMethods.GetRawTextFromURL.GetRawTextFromURL()
    files_select = ArticlesMethods.SelectPdfFilesLocal.SelectPdfFilesLocal()
    app = AppLogic.App.App(database, gigachat_methods, files_select, raw_text)
    from_date = datetime.date(2020, 1, 1)
    to_date = datetime.date(2021, 12, 31)
    app.add_data(from_date, to_date)
