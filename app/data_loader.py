from app.config import INVOICES_FILE
from app.exceptions import IdentificationError, InvalidAmountError

def load_invoices():
    invoices = []
    
    if not INVOICES_FILE.exists():
        raise FileNotFoundError(f"Файл не знайдено за шляхом: {INVOICES_FILE}")

    with open(INVOICES_FILE, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        
    for index, line in enumerate(lines[1:], start=2):
        try:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(",")
            invoice_id = parts[0]
            client = parts[1]
            amount_str = parts[2].strip()
            status = parts[3]
            
            if not amount_str:
                raise InvalidAmountError(f"Рядок {index}: поле суми пусте")
            
            amount = float(amount_str)
        
            if amount < 0:
                raise InvalidAmountError(f"Рядок {index}: сума від'ємна ({amount})")
            
            invoice_data = {
                "invoice_id": invoice_id,
                "client": client,
                "amount": amount,
                "status": status
            }
            invoices.append(invoice_data)
            
        except (ValueError, InvalidAmountError) as e:
            print(f"[ПОПЕРЕДЖЕННЯ] Пропускаємо рядок: {e}")
            
    return invoices