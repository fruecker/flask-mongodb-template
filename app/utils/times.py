"""Utility module that helps handling datetime and time"""
import datetime

def get_utc_now():
    """Get the current utc time.

    Returns:
        datetime: The current utc datetime
    """
    return datetime.datetime.utcnow()

def get_timestamp_from_datetime(datetime_obj:datetime.datetime):
    """Returns a timestamp from a datetime obj.

    Args:
        datetime_obj (datetime.datetime): The datetime object

    Returns:
        float: The timestamp of the datetime_obj
    """
    return datetime_obj.timestamp()

def get_date_plus_timedelta(datetime_obj, **timedelta_specs):
    """Adds the given timedelta to a datetime_obj.

    Args:
        datetime_obj (datetime.datetime): The datetime object
        timedelta_specs : The timedelta values

    Returns:
        datetime.datetime : The datetime_obj with the added timedelta
    """
    return datetime_obj + datetime.timedelta(**timedelta_specs)

def get_day_of_last_week(weekday:int=2):
    """Returns datetime obj of weekday of last week.

    Args:
        weekday (int, optional): The weekday. Defaults to 2 which is Wednesday.
    """
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday()-weekday, weeks=1)
