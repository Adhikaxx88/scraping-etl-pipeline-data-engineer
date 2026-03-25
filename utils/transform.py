import pandas as pd
import re

def transform_data(df):
    if df.empty:
        print("Empty Dataframe")
        return df

    try:
        
       
        df = df.drop_duplicates().dropna()

        df = df[df['title'] != "Unknown Product"]
        df = df[df['price'] != "Price Unavailable"]

        
        df['price'] = df['price'].apply(lambda x: float(re.sub(r'[^\d.]', '', str(x))) * 16000)

       
        df = df[~df['rating'].str.contains("Invalid", na=False)]
        df['rating'] = df['rating'].str.extract(r'(\d+\.\d+|\d+)').astype(float)

        df['colors'] = df['colors'].str.extract(r'(\d+)').astype(int)

       
        df['size'] = df['size'].str.replace('Size: ', '', case=False, regex=False)
        df['gender'] = df['gender'].str.replace('Gender: ', '', case=False, regex=False)

        df = df.reset_index(drop=True)
        
        print(f"Transformation Done: {len(df)} rows.")
        return df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()