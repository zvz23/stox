from dotenv import load_dotenv
import pyodbc
import os

load_dotenv()



CONNECTION_STRING = os.environ.get('CONNECTION_STRING')
def save_lead(lead_datas):
    with pyodbc.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO leads VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", lead_datas)