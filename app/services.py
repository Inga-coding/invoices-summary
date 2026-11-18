from app.data_loader import load_invoices

def calculate_total_amount(invoices):
    total = 0
    for inv in invoices:
        total += inv["amount"]
    return total

def get_unpaid_invoices(invoices):
    unpaid = []
    for inv in invoices:
        status = inv["status"].lower()
        if "очікується" in status or "прострочено" in status:
            unpaid.append(inv)
            
    return unpaid