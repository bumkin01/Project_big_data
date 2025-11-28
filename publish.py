import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine, text
import sys

def publish_data():
    print("Publish: Connecting to Database...")
    db_url = f"postgresql://admin:admin@db:5432/warehouse"
    engine = create_engine(db_url)

    try:
        query = text("SELECT * FROM production.processed_diabetes")
        df = pd.read_sql(query, engine)
        print(f"Publish: Read {len(df)} rows from Database.")
    except Exception as e:
        print(f"Error reading database: {e}")
        return

    # เชื่อมต่อ Google Sheets
    print("Publish: Connecting to Google Sheets...")
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
   
        sheet = client.open('Diabetes Dashboard Data')
        worksheet = sheet.get_worksheet(0)

        df = df.fillna('')
        
        data = [df.columns.values.tolist()] + df.values.tolist()

        worksheet.clear()
        worksheet.update(data)
        
        print("Publish: Success! Data uploaded to Google Sheets.")

    except Exception as e:
        print(f"Error uploading to Google Sheets: {e}")
        print("Tip: Did you share the Sheet with the client_email inside key.json?")

if __name__ == "__main__":
    publish_data()