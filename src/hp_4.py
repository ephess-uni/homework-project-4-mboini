# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date in old_dates:
        dt = datetime.strptime(date, '%Y-%m-%d')
        new_date = dt.strftime('%d %b %Y--%d %b %Y')
        new_dates.append(new_date)
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    delta = timedelta(days=1)
    return [start_dt + i*delta for i in range(n)]


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    # Set the fee schedule
    fees = {1: 0.50, 2: 1.00, 3: 2.00, 4: 3.00, 5: 4.00}

    # Read in the data from the input file
    with open(infile, 'r') as f:
        reader = DictReader(f)
        rows = list(reader)

    # Initialize the dictionary to store late fees
    late_fees = defaultdict(float)

    # Iterate over the rows of data
    for row in rows:
        # Get the due date and return date for the book
        due_date = row['due_date']
        return_date = row['return_date']

        # Re-format the dates
        due_date = datetime.strptime(due_date, '%Y-%m-%d')
        return_date = datetime.strptime(return_date, '%Y-%m-%d')

        # Determine the number of days late
        days_late = (return_date - due_date).days

        # Determine the patron ID and book type
        patron_id = int(row['patron_id'])
        book_type = int(row['book_type'])

        # Calculate the late fee for the book
        if days_late > 0:
            fee = fees[book_type] * days_late
            late_fees[patron_id] += fee

    # Write the summary report to the output file
    with open(outfile, 'w') as f:
        writer = DictWriter(f, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()

        for patron_id, fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': fee})


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.
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
