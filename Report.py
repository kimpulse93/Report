from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import matplotlib.pyplot as plt


# from gglshts import get_data
import pandas as pd

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '***********'
SAMPLE_RANGE_NAME = "'Данные'!A:O"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # print(values)
    return values


def kol_resh_vden(df):
    ds1 = df[['Номер', 'Дата решения', 'ЛП']]
    # Create Pivot table
    krd = ds1.pivot_table(index='Дата решения', columns='ЛП', values='Номер', aggfunc='count')
    #Build graph
    plt.figure(figsize=(20, 10))
    plt.plot(krd, color='green', marker='o', linestyle='--', markerfacecolor='blue')
    x = 0
    for i in krd.values:
        plt.text(krd.index[x], i[0]+20.0, "%d" % i[0], ha="center")
        plt.text(krd.index[x], i[1] + 20.0, "%d" % i[1], ha="center")
        x = x + 1
    plt.title("Кол-во Решенных на 1,2 ЛП", fontsize=14, fontweight="bold")
    plt.xlabel("Дата решения", fontsize=14, fontweight="bold")
    plt.ylabel("Кол-во", fontsize=14, fontweight="bold")
    plt.grid(True)
    plt.savefig('krd.png')
    return krd

def kol_resh_vden_proc(df):
    x = 0
    ds1 = df[['Номер', 'Дата решения', 'ЛП']]
    krd = ds1.pivot_table(index='Дата решения', columns='ЛП', values='Номер',
                          aggfunc='count')  # колво решенных на 1 2лп
    a = krd
    a['3'] = a['1'] / (a['1'] + a['2']) * 100
    prd = a[['3']]
    plt.figure(figsize=(18, 7))
    plt.plot(prd, color='red', marker='o', linestyle='--', markerfacecolor='blue')
    plt.grid(True)
    plt.title("Ежедневный процент Решенных на 1ЛП", fontsize=14, fontweight="bold")
    plt.xlabel("Дата решения", fontsize=14, fontweight="bold")
    plt.ylabel("Процент", fontsize=14, fontweight="bold")
    for i in prd.values:
        plt.text(prd.index[x], i[0]+0.5, "%d" % i[0], ha="center")
        x = x + 1
    plt.savefig('prd.png')
    return prd


def kol_vozvr(df):
    ds3 = df[['Количество возвратов на доработку', 'Исполнитель', 'Номер', 'ЛП']]
    a = ds3.query('ЛП == "1"')
    s = a.pivot_table(index='Исполнитель', columns='Количество возвратов на доработку', values='Номер', aggfunc='count')
    print(s)
    ds4 = pd.DataFrame(s.to_records()).fillna(0)
    ds4['summa'] = ds4['1'] + ds4['2'] + ds4['3']
    d5 = ds4[['Исполнитель', 'summa']]
    print(d5)
    d5.plot.bar('Исполнитель', 'summa',  figsize=(20, 12))
    plt.savefig('d5.png')
    return d5, ds4



if __name__ == '__main__':
    data = main()
    # Transformation for dataframe
    df = pd.DataFrame(data[1:], columns=data[0])
    kol_vozvr(df)
























