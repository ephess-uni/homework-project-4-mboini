from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date in old_dates:
        new_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y')
        new_dates.append(new_date)
    return new_dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    dates = []
    for i in range(n):
        date = datetime.strptime(start, '%Y-%m-%d') + timedelta(days=i)
        dates.append(date)
    return dates

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_range = date_range(start_date, len(values))
    result = [(date, value) for date, value in zip(date_range, values)]
    return result

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as file:
        data = list(DictReader(file))
        for item in data:
            date_returned = datetime.strptime(item['date_returned'], '%m/%d/%Y')
            date_due = datetime.strptime(item['date_due'], '%m/%d/%Y')
            days_late = (date_returned - date_due).days
            if days_late > 0:
                late_fee = round(days_late * 0.25, 2)
            else:
                late_fee = 0.0
            item['late_fees'] = late_fee
        aggregated_data = defaultdict(float)
        for item in data:
            patron_id = item['patron_id']
            late_fees = item['late_fees']
            aggregated_data[patron_id] += late_fees
        results = [{'patron_id': key, 'late_fees': value} for key, value in aggregated_data.items()]
        for result in results:
            result['late_fees'] = '{:.2f}'.format(result['late_fees'])
    with open(outfile, 'w', newline='') as file:
        columns = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

if __name__ == '__main__':
    from util import get_data_file_path
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')
    OUTFILE = 'book_fees.csv'
    fees_report(BOOK_RETURNS_PATH, OUTFILE)
    with open(OUTFILE) as file:
        print(file.read())
