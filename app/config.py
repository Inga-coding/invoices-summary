from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
Data_DIR = BASE_DIR / "data"
INVOICES_FILE = Data_DIR / "invoices.csv"