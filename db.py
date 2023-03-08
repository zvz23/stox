from dotenv import load_dotenv
import pyodbc
import os

load_dotenv()

SERVER = os.environ.get('SERVER')
DATABASE=os.environ.get('DATABASE')
USERNAME=os.environ.get('USERNAMEDB')
PASSWORD=os.environ.get('PASSWORD')
DRIVER=os.environ.get('DRIVER')


CONNECTION_STRING = "<CONNECTION STRING HERE>"
def save_lead(lead_datas):
    with pyodbc.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO leads VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", lead_datas)