import pandas as pd
from sqlalchemy import create_engine
import gspread
from google.oauth2.service_account import Credentials
import os
import json

def load_to_csv(df):
    try:
        target_dir = "result"
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        file_path = os.path.join(target_dir, "products.csv")
        
        # 4. Save!
        df.to_csv(file_path, index=False)
        print(f"Done : {file_path}")
        
    except Exception as e:
        print(f"Fail: {e}")


def load_to_gsheets(df, json_key_path, spreadsheet_name):

    try:

        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(json_key_path, scopes=scope)
        client = gspread.authorize(creds)

        sh = client.open(spreadsheet_name)
        worksheet = sh.get_worksheet(0) # Ambil sheet pertama

        worksheet.clear()


        header = [df.columns.values.tolist()]
        values = df.values.tolist()
        data_to_upload = header + values


        worksheet.update(data_to_upload)
        

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Undefined '{spreadsheet_name}' !.")
    except Exception as e:
        print(f"Failed to load: {e}")
        

def get_db_config(file_path='credentials.json'):

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Ambil data yang tadi lu selipin di bawah
            return {
                "user": data.get('db_user'),
                "pw": data.get('db_password'),
                "db": data.get('db_name'),
                "host": data.get('db_host', 'localhost'),
                "port": data.get('db_port', '5432')
            }
    except Exception as e:
        print(f"Failed to read credentials.json: {e}")
        return None

def load_to_postgres(df):

    config = get_db_config()
    
    if not config or not config['user']:
        print("Config DB Failed!")
        return

    try:

        
   
        url = f"postgresql://{config['user']}:{config['pw']}@{config['host']}:{config['port']}/{config['db']}"
        engine = create_engine(url)
        
        with engine.begin() as connection:
            df.to_sql('fashion_products', con=connection, if_exists='replace', index=False)
            print("Done!")
        
    except Exception as e:
        print(f" Error Load Postgres: {e}")