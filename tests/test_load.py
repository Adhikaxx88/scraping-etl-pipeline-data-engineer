import pytest
import pandas as pd
import json
from unittest.mock import patch, MagicMock, mock_open
from utils.load import get_db_config, load_to_postgres, load_to_csv, load_to_gsheets

def test_get_db_config_success():
    """Tes apakah fungsi bisa baca kredensial JSON dengan benar."""
    mock_json = '{"db_user": "adhika", "db_password": "123", "db_name": "test_db"}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        config = get_db_config('fake_path.json')
        assert config['user'] == "adhika"
        assert config['db'] == "test_db"

@patch('utils.load.create_engine')
@patch('utils.load.get_db_config')
def test_load_to_postgres_execution(mock_config, mock_engine):
    """Tes proses upload ke PostgreSQL menggunakan mocking."""
    mock_config.return_value = {'user': 'a', 'pw': 'b', 'db': 'c', 'host': 'h', 'port': 'p'}
    mock_conn = MagicMock()
    # Mocking 'with engine.begin() as connection'
    mock_engine.return_value.begin.return_value.__enter__.return_value = mock_conn
    
    df = pd.DataFrame({'test': [1]})
    load_to_postgres(df)
    
    # Pastikan transaksi DB dimulai
    assert mock_engine.return_value.begin.called

@patch('utils.load.os.path.exists')
@patch('utils.load.os.makedirs')
@patch('pandas.DataFrame.to_csv')
def test_load_to_csv_success(mock_to_csv, mock_makedirs, mock_exists):
    """Tes fungsi load_to_csv agar baris direktorinya ter-cover."""
    mock_exists.return_value = False
    df = pd.DataFrame({'test': [1]})
    load_to_csv(df)
    # Pastikan folder dibuat dan fungsi to_csv terpanggil
    assert mock_makedirs.called
    assert mock_to_csv.called

@patch('utils.load.gspread.authorize')
@patch('utils.load.Credentials.from_service_account_file')
def test_load_to_gsheets_mock(mock_creds, mock_gspread):
    """Tes fungsi gsheets agar baris library gspread ter-cover."""
    mock_client = MagicMock()
    mock_gspread.return_value = mock_client
    df = pd.DataFrame({'test': [1]})
    
    # Jalankan fungsi
    load_to_gsheets(df, 'fake.json', 'fake_sheet')
    
    # Pastikan library Google Auth & Gspread terpanggil
    assert mock_creds.called
    assert mock_gspread.called