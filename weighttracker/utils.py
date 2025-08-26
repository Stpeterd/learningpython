from datetime import datetime, timedelta

def get_current_week_start_end():
    today = datetime.now()
    # Monday is 0, Sunday is 6
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')

def get_previous_week_start_end():
    today = datetime.now()
    # Monday is 0, Sunday is 6
    start_of_current_week = today - timedelta(days=today.weekday())
    start_of_previous_week = start_of_current_week - timedelta(weeks=1)
    end_of_previous_week = start_of_previous_week + timedelta(days=6)
    return start_of_previous_week.strftime('%Y-%m-%d'), end_of_previous_week.strftime('%Y-%m-%d')

def get_current_date_str():
    return datetime.now().strftime('%Y-%m-%d')

def format_weight(weight):
    return f"{weight:.1f}"


