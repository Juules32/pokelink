from datetime import date, datetime, timedelta

def get_date(delta: int = 0) -> date:
    return datetime.today().date() + timedelta(days=delta)

def format_date(date: date) -> str:
    return date.strftime('%Y-%m-%d')

def to_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def types_in_common(itypes: set[str], jtypes: set[str]) -> bool:
    return not itypes.isdisjoint(jtypes)
