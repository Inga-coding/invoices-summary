from app.data_loader import load_invoices
from app.services import calculate_total_amount, get_unpaid_invoices

def main():
    print("ЗАПУСК ПРОГРАМИ ОБРОБКИ РАХУНКІВ")
    
    try:
        invoices = load_invoices()
        print(f"\nУспішно завантажено та перевірено рахунків: {len(invoices)}")
    
        print("\nСписок коректних рахунків:")
        for inv in invoices:
            print(f"ID: {inv['invoice_id']} | Клієнт: {inv['client']} | Сума: {inv['amount']} грн | Статус: {inv['status']}")
         
        total = calculate_total_amount(invoices)
        print(f"\nЗагальна сума всіх успішних рахунків: {total} грн")
        
        unpaid = get_unpaid_invoices(invoices)
        print(f"\nКількість неоплачених/прострочених рахунків: {len(unpaid)}")
        for inv in unpaid:
            print(f"ID: {inv['invoice_id']} | Клієнт: {inv['client']} | Сума: {inv['amount']} грн | Статус: {inv['status']}")
            
    except Exception as e:
        print(f"\n[КРИТИЧНА ПОМИЛКА]: {e}")

if __name__ == "__main__":
    main()