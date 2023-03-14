from sheets import append_rows
from dotenv import load_dotenv
import os

load_dotenv()
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')

append_rows(SPREADSHEET_ID, 'Sheet1' ,[['test', 'test']])