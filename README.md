# Scraping ETL Pipeline: Fashion Studio Competitor Analysis
An automated End-to-End ETL Pipeline designed to extract, transform, and load retail competitor data from web sources to multiple data repositories.

## 🚀 Project Overview
This project acts as a competitive intelligence tool for a fashion retail company. It monitors **Fashion Studio** (competitor) by scraping product details across 50 pages and processing them into a ready-to-use format for Data Science teams.

### Key Features:
* **Modular Architecture**: Separated Extract, Transform, and Load modules.
* **Robust Scraping**: Handles 1000+ data entries with built-in error handling and timestamps.
* **Data Cleaning**: Automated currency conversion (USD to IDR), duplicate removal, and regex-based string cleaning.
* **Multi-Repo Loading**: Supports CSV, PostgreSQL, and Google Sheets API integration.
* **High Test Coverage**: Unit testing implemented using Pytest with >80% coverage.

## 🛠️ Tech Stack
* **Language**: Python 3.13
* **Libraries**: Requests, BeautifulSoup4, Pandas, SQLAlchemy, Gspread
* **Storage**: PostgreSQL, Google Sheets, Flat File (CSV)
* **Testing**: Pytest, Pytest-cov

## 🏗️ Architecture Diagram


## 📂 Project Structure
```text
submission-pemda/
├── tests/              # Unit testing scripts
├── utils/
│   ├── extract.py      # Web Scraping logic
│   ├── transform.py    # Data cleaning & transformation
│   └── load.py         # Multi-repository loading logic
├── main.py             # Pipeline entry point
├── requirements.txt    # Project dependencies
└── credentials.json    # Google Service Account (Hidden via .gitignore)
