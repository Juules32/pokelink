from datetime import datetime, timedelta

def get_datetime(delta: int = 0) -> datetime:
    return datetime.today() + timedelta(days=delta)

def get_date_str(delta: int = 0) -> str:
    return get_datetime(delta).strftime('%Y-%m-%d')
