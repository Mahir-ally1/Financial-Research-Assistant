from datetime import date

def get_most_recent_quarter() -> str:
    """Returns the most recent completed fiscal quarter in the form YYYYQX."""
    today = date.today()
    year = today.year
    month = today.month

    if month <= 3:
        quarter = 4
        year -= 1
    elif month <= 6:
        quarter = 1
    elif month <= 9:
        quarter = 2
    else:
        quarter = 3
    return f"{year}Q{quarter}"
