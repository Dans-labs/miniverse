"""
Convenience methods for date formatting
"""
from datetime import datetime, date
import calendar


DATE_DELIM = '-'
TIMESTAMP_MASK = '%Y-%m-%d %H:%M:%S'
TIMESTAMP_MASK_FOR_FILE = '%Y-%m-%d_%H-%M-%S'


def get_timestamp_for_filename():

    return datetime.now().strftime(TIMESTAMP_MASK_FOR_FILE)

def format_yyyy_mm_dd(date_str, delim=DATE_DELIM):
    """Convert a string in YYYY-MM-DD format to a datetime object"""

    try:
        return True, datetime.strptime(date_str,\
            '%Y{0}%m{0}%d'.format(delim))
    except ValueError:
        return False, 'Date not in YYYY{0}MM{0}DD format'.format(DATE_DELIM)


def get_month_name_abbreviation(month_num):
    """Convert a month integer, between 1 and 12, to a month name"""
    try:
        return True, calendar.month_abbr[month_num]
    except IndexError:
        return False, 'The month number must be between 1 and 12'
    except TypeError:
        return False, 'The month must be a *number* between 1 and 12'
    except:
        return False, 'The month must be a *number* between 1 and 12'

def get_month_name(month_num):
    """Convert a month integer, between 1 and 12, to a month name"""
    try:
        return True, calendar.month_name[month_num]
    except IndexError:
        return False, 'The month number must be between 1 and 12'
    except TypeError:
        return False, 'The month must be a *number* between 1 and 12'
    except:
        return False, 'The month must be a *number* between 1 and 12'


def get_one_year_ago(date_now):
    """Used for metrics visualizations, showing last 12 months"""
    assert isinstance(date_now, datetime) or isinstance(date_now, date),\
        'date_now must be a datetime.datetime or datetime.date object'

    if date_now.month == 12:
        year_ago_month = 1
        year_ago_year = date_now.year
    else:
        year_ago_month = date_now.month + 1
        year_ago_year = date_now.year - 1

    one_year_ago = datetime(year_ago_year, year_ago_month, 1)
    return one_year_ago


def month_year_iterator( start_month, start_year, end_month, end_year ):
    """Return a month year iterator:
    g = month_year_iterator(01, 2013, 5, 2014)
        g.next()
        (2013, 1)
        g.next()
        (2013, 2), etc

    source: http://stackoverflow.com/questions/5734438/how-to-create-a-month-iterator
    """
    ym_start = 12 * start_year + start_month - 1
    ym_end= 12 * end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m+1
