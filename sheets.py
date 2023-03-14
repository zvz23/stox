import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow



SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def append_row(sheet_id, sheet_name, row):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet_range = sheet_name + '!A:A'
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=sheet_range, valueInputOption='RAW', insertDataOption='INSERT_ROWS', body={'values': [row]}).execute()
    print('{0} cells appended to sheet.'.format(result.get('updates').get('updatedCells')))


def append_rows(sheet_id, sheet_name, values):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    # Get the current number of rows in the sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=sheet_name
    ).execute()
    num_rows = len(result.get('values', []))

    # Calculate the range to append to
    start_range = f"A{num_rows+1}"
    end_range = f"A{num_rows+len(values)}"
    # Set the request body
    value_input_option = 'USER_ENTERED' # interpret values as user-entered (vs. raw)
    insert_data_option = 'INSERT_ROWS' # insert new rows, shifting down existing ones

    value_range_body = {
        'range': start_range + ':' + end_range,
        'majorDimension': 'ROWS',
        'values': values
    }

    # Call the Sheets API to append the data
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=start_range + ':' + end_range,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=value_range_body
    ).execute()
    print(f"{result.get('updates', {}).get('updatedRows', 0)} rows appended to {sheet_name}")
