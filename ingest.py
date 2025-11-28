import pandas as pd
from sqlalchemy import create_engine
import time
import os

def ingest_data():
    file_path = "./data/diabetes_dataset.csv"
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    df = pd.read_csv(file_path)
    df.columns = [c.replace(":", "") for c in df.columns]

    engine = create_engine(f"postgresql://admin:admin@db:5432/warehouse")

    retries = 20
    while retries > 0:
        try:
            with engine.connect() as conn:
                break
        except Exception:
            print("Ingest: DB not ready, retry in 5s...")
            time.sleep(5)
            retries -= 1

    # Save ลง public.raw_data_diabetes
    df.to_sql('raw_data_diabetes', engine, if_exists='replace', index=False)
    print("Ingest: Data loaded successfully to table 'raw_data_diabetes'")

if __name__ == "__main__":
    ingest_data()
