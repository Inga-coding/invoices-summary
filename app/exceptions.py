class InvalidAmountError(Exception):
    """Виняток, який спрацьовує, якщо сума в документі некоректна (порожня, текст або мінус)."""
    pass
class IdentificationError(Exception):
    """Виняток при помилці ідентифікації рахунку."""
    pass