from app.config import INVOICES_FILE
from app.exceptions import IdentificationError, InvalidAmountError


def parse_invoice_lines(lines, strict: bool = False):
    invoices = []

    if not lines:
        return invoices

    for index, line in enumerate(lines[1:], start=2):
        try:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) < 4:
                raise IdentificationError(f"Рядок {index}: недостатньо колонок (очікується 4)")

            invoice_id = parts[0].strip()
            client = parts[1].strip()
            amount_str = parts[2].strip()
            status = parts[3].strip()

            if not invoice_id:
                raise IdentificationError(f"Рядок {index}: відсутній ID рахунку")

            if not amount_str:
                raise InvalidAmountError(f"Рядок {index}: поле суми пусте")

            amount = float(amount_str)

            if amount < 0:
                raise InvalidAmountError(f"Рядок {index}: сума від'ємна ({amount})")

            invoice_data = {
                "invoice_id": invoice_id,
                "client": client,
                "amount": amount,
                "status": status,
            }
            invoices.append(invoice_data)

        except (ValueError, InvalidAmountError, IdentificationError) as e:
            if strict:
                raise
            print(f"[ПОПЕРЕДЖЕННЯ] Пропускаємо рядок: {e}")

    return invoices


def load_invoices(file_path=INVOICES_FILE, strict: bool = False):
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не знайдено за шляхом: {file_path}")

    with open(file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    return parse_invoice_lines(lines, strict=strict)