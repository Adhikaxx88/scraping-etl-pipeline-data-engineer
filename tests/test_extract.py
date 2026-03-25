import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.extract import scraping, extract_main

@patch('requests.get')
def test_scraping_success(mock_get):
    """Mengetes skenario scraping berhasil mengambil data."""
    # Simulasi respon HTML dari website
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <div class="collection-card">
        <h3>Kaos Keren</h3>
        <p class="price">$10.00</p>
        <p>Rating: 4.5 / 5</p>
        <p>Colors: 3 Colors</p>
        <p>Size: XL</p>
        <p>Gender: Men</p>
    </div>
    """
    mock_get.return_value = mock_response

    result = scraping(1)
    assert len(result) == 1
    assert result[0]['title'] == "Kaos Keren"
    assert "timestamp" in result[0]

@patch('requests.get')
def test_scraping_fail(mock_get):
    """Mengetes skenario scraping gagal karena timeout/internet mati."""
    mock_get.side_effect = Exception("Timeout")
    result = scraping(999)
    # Harus return list kosong, bukan crash
    assert result == []

@patch('utils.extract.scraping')
def test_extract_main_flow(mock_scraping):
    """Mengetes fungsi utama extract_main agar looping terhitung di coverage."""
    # Kembalikan list kosong agar proses test kilat
    mock_scraping.return_value = []
    
    # Kita mock time.sleep biar gak perlu nunggu delay 0.1 detik per halaman
    with patch('utils.extract.time.sleep'): 
        df = extract_main()
    
    assert isinstance(df, pd.DataFrame)
    assert mock_scraping.call_count == 50 # Pastiin dia beneran loop 50 kali