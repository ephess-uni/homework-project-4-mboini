# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date_str in old_dates:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = date.strftime('%d %b %Y')
        new_dates.append(new_date_str)
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError('start must be a string')
    if not isinstance(n, int):
        raise TypeError('n must be an integer')

    dates = []
    current_date = datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        dates.append(current_date)
        current_date += timedelta(days=1)

    return dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    
    late_fees = defaultdict(float)

    
    with open(infile, 'r') as f:
        reader = DictReader(f)

        
        for row in reader:
            if 'due_date' not in row:
                continue
            due_date = datetime.strptime(row['due_date'], '%Y-%m-%d')
            return_date = datetime.strptime(row['return_date'], '%Y-%m-%d')
            if return_date > due_date:
                days_late = (return_date - due_date).days
                late_fee = days_late * 0.25
                patron_id = row['patron_id']
                late_fees[patron_id] += late_fee

    
    with open(outfile, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, late_fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': late_fee})



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
