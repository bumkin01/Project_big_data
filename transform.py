import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import time

def transform_data():
    # สร้าง Connection String
    db_url = f"postgresql://admin:admin@db:5432/warehouse"
    engine = create_engine(db_url)

    # Retry until table exists
    retries = 20
    df_raw = pd.DataFrame()
    
    print("Transform: Waiting for data ingestion...")
    while retries > 0:
        try:
            query = text("SELECT * FROM raw_data_diabetes")
            df_raw = pd.read_sql(query, engine)
            
            if not df_raw.empty:
                print("Transform: Data found!")
                break
        except Exception as e:
            print(f"Table not ready, retry in 5s... ({e})")
            time.sleep(5)
            retries -= 1

    if df_raw.empty:
        print("Error: Could not fetch data from database.")
        return

    df = df_raw.copy()

    race_cols = ["race_AfricanAmerican","race_Asian","race_Caucasian","race_Hispanic","race_Other"]
    existing_race_cols = [c for c in race_cols if c in df.columns]
    
    if existing_race_cols:
        df_race = df[existing_race_cols]
        df['Race'] = df_race.idxmax(axis=1).str.replace("race_", "", regex=False).str.replace("AfricanAmerican","African-American")
        df = df.drop(columns=existing_race_cols)

    # Age group
    bins_age = [0, 18, 25, 35, 45, 55, 65, np.inf]
    age_order = ["0-18","18-24","25-34","35-44","45-54","55-64","65+"]
    df['Age Group'] = pd.cut(df['age'], bins=bins_age, labels=age_order)

    # BMI category
    bins_bmi = [0, 18.5, 25, 30, 35, 40, np.inf]
    bmi_order = ["Underweight","Normal","Overweight","Moderately Obese","Severely Obese","Morbidly Obese"]
    df['BMI Category'] = pd.cut(df['bmi'], bins=bins_bmi, labels=bmi_order)

    # Smoking cleanup
    df['Smoking History'] = df['smoking_history'].str.title()
    df = df[df['Smoking History'] != "No Info"]

    # Select and Rename Columns
    cols_to_keep = ['year','gender','Race','Age Group','location','hypertension','heart_disease','Smoking History','bmi','BMI Category','hbA1c_level','blood_glucose_level','diabetes']
    
    # Filter เฉพาะ column ที่มีอยู่จริง (เผื่อ race หายไป)
    cols_to_keep = [c for c in cols_to_keep if c in df.columns]
    
    df_final = df[cols_to_keep].copy()
    
    rename_map = {
        'year':'Year','gender':'Gender','location':'Location','hypertension':'Hypertension','heart_disease':'Heart Disease',
        'bmi':'BMI','hbA1c_level':'HbA1C Level','blood_glucose_level':'Blood Glucose Level','diabetes':'Diabetes'
    }
    df_final = df_final.rename(columns=rename_map)

    
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS production;"))
        conn.commit()

    df_final.to_sql("processed_diabetes", engine, schema="production", if_exists="replace", index=False)
    print("Data transformed and loaded → production.processed_diabetes")

if __name__ == "__main__":
    transform_data()
