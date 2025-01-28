def validate_phone(value):
    """Validate phone number format"""
    return value.isdigit() or value == ""

def validate_date(value):
    """Validate date format (YYYY-MM-DD)"""
    parts = value.split("-")
    if len(parts) != 3:
        return False
    try:
        year, month, day = map(int, parts)
        return 1 <= month <= 12 and 1 <= day <= 31 and year > 1930
    except ValueError:
        return False