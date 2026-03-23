from utils.extract import extract_main
from utils.load import transform_data
def main():
   df_raw = extract_main()
   df_clean = transform_data(df_raw)
   print(df_clean.head())
   print(df_clean.info())

if __name__ == "__main__":
    main()
