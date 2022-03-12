import re

def validate_date(date_str):
    is_valid = re.search('^\d{1,2}\/\d{1,2}\/\d{4}$', date_str)
    return bool(is_valid)

def validate_datetime(datetime_str):
    is_valid = re.search('^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{1,2}$', datetime_str)
    return bool(is_valid)

def validate_time(time_str):
    is_valid = re.search('^\d{1,2}:\d{1,2}$', time_str)
    return bool(is_valid)