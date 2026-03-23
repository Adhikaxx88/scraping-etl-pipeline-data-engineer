import pandas as pd
import re

def transform_data(df):
    if df.empty:
        print("Empty Dataframe")
        return df

    try:
        
        # 1. Buang Duplikat dan Data Kosong (Null)
        df = df.drop_duplicates().dropna()

        # 2. Filter data invalid (Unknown Product & Price Unavailable)
        df = df[df['title'] != "Unknown Product"]
        df = df[df['price'] != "Price Unavailable"]

        # 3. Transform PRICE: Hilangkan '$', ubah ke float, kalikan 16.000
        # Pakai regex r'[^\d.]' untuk buang semua karakter kecuali angka dan titik
        df['price'] = df['price'].apply(lambda x: float(re.sub(r'[^\d.]', '', str(x))) * 16000)

        # 4. Transform RATING: Ambil angka depan (misal 4.8 / 5 -> 4.8)
        # Kita filter juga "Invalid Rating" agar tidak error
        df = df[~df['rating'].str.contains("Invalid", na=False)]
        df['rating'] = df['rating'].str.extract(r'(\d+\.\d+|\d+)').astype(float)

        # 5. Transform COLORS: Ambil angkanya saja (3 Colors -> 3)
        df['colors'] = df['colors'].str.extract(r'(\d+)').astype(int)

        # 6. Transform SIZE & GENDER: Hapus prefix teks
        df['size'] = df['size'].str.replace('Size: ', '', case=False, regex=False)
        df['gender'] = df['gender'].str.replace('Gender: ', '', case=False, regex=False)

        # Reset index agar rapi setelah ada baris yang dibuang
        df = df.reset_index(drop=True)
        
        print(f"Transformation Done: {len(df)} rows.")
        return df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()