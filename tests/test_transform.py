import pandas as pd
from utils.transform import transform_data

def test_transform_full_logic():
    # Data dummy kotor sesuai kriteria Reject/Basic
    raw_data = {
        'title': ['Kaos Polos', 'Unknown Product', 'Kaos Polos'], # Ada duplikat & Unknown
        'price': ['$10.00', '$20.00', '$10.00'],
        'rating': ['4.8 / 5', 'Invalid Rating', '4.8 / 5'],
        'colors': ['3 Colors', '2 Colors', '3 Colors'],
        'size': ['Size: XL', 'Size: L', 'Size: XL'],
        'gender': ['Gender: Men', 'Gender: Women', 'Gender: Men']
    }
    df = pd.DataFrame(raw_data)
    
    df_clean = transform_data(df)

    # 1. Cek Duplikat & Unknown dibuang
    assert len(df_clean) == 1 
    
    # 2. Cek Kurs Rp16.000 ($10 * 16.000 = 160.000)
    assert df_clean['price'].iloc[0] == 160000.0
    
    # 3. Cek Rating jadi float 4.8
    assert df_clean['rating'].iloc[0] == 4.8
    assert isinstance(df_clean['rating'].iloc[0], float)

    # 4. Cek Colors jadi int 3
    assert df_clean['colors'].iloc[0] == 3
    
    # 5. Cek Size & Gender bersih dari prefix
    assert df_clean['size'].iloc[0] == 'XL'
    assert df_clean['gender'].iloc[0] == 'Men'

def test_transform_empty():
    df_empty = pd.DataFrame()
    result = transform_data(df_empty)
    assert result.empty