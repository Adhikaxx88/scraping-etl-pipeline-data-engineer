from utils.extract import extract_main
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_gsheets
def main():
   df_raw = extract_main()
   df_clean = transform_data(df_raw)
   print(df_clean.head())
   print(df_clean.info())
   load_to_csv(df_clean)
   load_to_gsheets(df_clean,"credentials.json", "dicoding-project")

if __name__ == "__main__":
    main()
