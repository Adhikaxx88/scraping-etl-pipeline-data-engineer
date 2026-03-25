import requests 
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

def scraping(page_number):

    if page_number == 1:
        url = "https://fashion-studio.dicoding.dev/index.html"
    else:
        url = f"https://fashion-studio.dicoding.dev/page{page_number}"
    
    try: 
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
  
        items = soup.find_all('div', class_='collection-card')
        
        for item in items:

            title = item.find('h3').get_text(strip=True) if item.find('h3') else "Unknown Product"

            price = item.find(class_='price').get_text(strip=True) if item.find(class_='price') else None
            p_tags = item.find_all('p')

            rating = next((p.get_text(strip=True) for p in p_tags if "Rating" in p.text), None)
            colors = next((p.get_text(strip=True) for p in p_tags if "Colors" in p.text), None)
            size = next((p.get_text(strip=True) for p in p_tags if "Size" in p.text), None)
            gender = next((p.get_text(strip=True) for p in p_tags if "Gender" in p.text), None)

            products.append({
                'title': title,
                'price': price,
                'rating': rating,
                'colors': colors,
                'size': size,
                'gender': gender,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
                
        return products
    except Exception as e:
        print(f"Error di halaman {page_number}: {e}")
        return []
def extract_main():
    all_data = []
    
    for i in range (1,51):
        data_dari_halaman = scraping(i)
        all_data.extend(data_dari_halaman)
        time.sleep(0.1)
        
        if i%10==0:
            print(f"page{i} done")
    df = pd.DataFrame(all_data)
    print(f"Total data: {len(df)}")
    return df
if __name__ == "__main__":
    df_mentah = extract_main()
    print(df_mentah.head()) 