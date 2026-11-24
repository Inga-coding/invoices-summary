from app.services import calculate_total_amount, get_unpaid_invoices


def test_calculate_total_amount():
    invoices = [
        {"amount": 1000.0, "status": "оплачено"},
        {"amount": 2500.5, "status": "очікується"},
        {"amount": 500.0, "status": "прострочено"},
    ]
    assert calculate_total_amount(invoices) == 4000.5


def test_calculate_total_amount_empty():
    assert calculate_total_amount([]) == 0


def test_get_unpaid_invoices():
    invoices = [
        {"id": 1, "amount": 1000.0, "status": "оплачено"},
        {"id": 2, "amount": 2500.0, "status": "Очікується"},
        {"id": 3, "amount": 500.0, "status": "прострочено"},
    ]
    unpaid = get_unpaid_invoices(invoices)
    assert len(unpaid) == 2
    assert [inv["id"] for inv in unpaid] == [2, 3]