import os
import sys
import warnings

from datetime import datetime

from InquirerPy import inquirer
from InquirerPy.validator import NumberValidator
from dotenv import load_dotenv

from AppLogic.App import App
from ArticlesMethods.GetRawTextFromURL import GetRawTextFromURL
from ArticlesMethods.SelectPdfFilesLocal import SelectPdfFilesLocal
from DatabaseMethods.DatabaseMethodsImpl import DatabaseMethods
from GigaChainMethods.GigaChainMethodsImpl import GigaChainMethodsImpl
from Visualize.VisualizeImpl import VisualizeImpl

warnings.filterwarnings("ignore")
load_dotenv()
API_KEY = os.getenv("API_KEY")

def run_console():
    conn_string = "dbname=sber-hack-database user=admin password=admin host=localhost port=2432"
    database = DatabaseMethods(conn_string)
    gigachat_methods = GigaChainMethodsImpl(API_KEY)
    raw_text = GetRawTextFromURL()
    files_select = SelectPdfFilesLocal()
    visualize = VisualizeImpl()

    app = App(database, gigachat_methods, files_select, raw_text)

    while True:
        action = inquirer.select(
            message="What do you want to do?",
            choices=['Add data', 'Compare data', 'Exit'],
            pointer=">"
        ).execute()

        if action == 'Add data':
            from_date = inquirer.text(
                message="Enter start date (YYYY-MM-DD):",
                validate=lambda x: datetime.strptime(x, '%Y-%m-%d')
            ).execute()
            to_date = inquirer.text(
                message="Enter end date (YYYY-MM-DD):",
                validate=lambda x: datetime.strptime(x, '%Y-%m-%d')
            ).execute()
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            app.add_data(from_date, to_date)
            print("Data added successfully!")

        elif action == 'Compare data':
            data_method = inquirer.select(
                message="Select data retrieval method:",
                choices=['By Year', 'By Month and Year'],
                pointer=">"
            ).execute()

            topics = []
            time_frame = ''
            data = None
            if data_method == 'By Year':
                year = inquirer.text(
                    message="Enter year to compare data:",
                    validate=NumberValidator()
                ).execute()
                data = database.extract_topics_by_year(int(year))
                time_frame = f"year_{year}"
                if data.empty:
                    print("There is no data for the selected period.")
                    continue
            elif data_method == 'By Month and Year':
                year = inquirer.text(message="Enter year:", validate=NumberValidator()).execute()
                month = inquirer.text(message="Enter month:", validate=NumberValidator()).execute()
                data = database.extract_topics_by_month_year(int(year), int(month))
                time_frame = f"year_{year}_month_{month}"
                if data.empty:
                    print("There is no data for the selected period.")
                    continue

            compare_type = inquirer.select(
                message="Choose comparison type:",
                choices=['Single', 'Multiple'],
                pointer=">"
            ).execute()

            if compare_type == 'Single':
                topic_choices = data['name'].unique().tolist()
                topic_name = inquirer.select(
                    message="Select a topic:",
                    choices=topic_choices,
                ).execute()
                specific_topic_data = data[data['name'] == topic_name]
                filename = f"{topic_name}_comparison_{time_frame}.png"
                visualize.compare_single(specific_topic_data, topic_name, time_frame, filename)
                print(f"Single comparison for '{topic_name}' saved as {filename}")

            elif compare_type == 'Multiple' and data is not None:
                filename = f"all_topics_comparison_{time_frame}.png"
                visualize.compare_multiple(data, time_frame, filename)
                print(f"Multiple comparison for all topics saved as {filename}")

        elif action == 'Exit':
            print("Exiting...")
            sys.exit()

        else:
            print("Invalid choice. Please select a valid option.")
