from app.data_loader import load_invoices
from app.exceptions import InvalidAmountError
from app.services import calculate_total_amount, get_unpaid_invoices


def main():
    print("ЗАПУСК ПРОГРАМИ ОБРОБКИ РАХУНКІВ")

    try:
        invoices = load_invoices()
        print(f"\nУспішно завантажено та перевірено рахунків: {len(invoices)}")

        print("\nСписок коректних рахунків:")
        for inv in invoices:
            print(
                f"ID: {inv['invoice_id']} | Клієнт: {inv['client']} | "
                f"Сума: {inv['amount']} грн | Статус: {inv['status']}"
            )

        total = calculate_total_amount(invoices)
        print(f"\nЗагальна сума всіх успішних рахунків: {total} грн")

        unpaid = get_unpaid_invoices(invoices)
        print(f"\nКількість неоплачених/прострочених рахунків: {len(unpaid)}")
        for inv in unpaid:
            print(
                f"ID: {inv['invoice_id']} | Клієнт: {inv['client']} | "
                f"Сума: {inv['amount']} грн | Статус: {inv['status']}"
            )

    except FileNotFoundError as e:
        print(f"\n[ПОМИЛКА ФАЙЛУ]: Файл із даними не знайдено — {e}")
    except (IdentificationError,InvalidAmountError, ValueError, KeyError, IndexError, TypeError) as e:
        print(f"\n[ПОМИЛКА ДАНИХ]: Проблема з даними або структурою рахунків — {e}")


if __name__ == "__main__":
    main()