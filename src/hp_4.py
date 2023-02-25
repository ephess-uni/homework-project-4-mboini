import datetime

def reformat_dates(dates):
    new_dates = []
    for date in dates:
        datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        new_date = datetime_obj.strftime('%d %b %Y')
        new_dates.append(new_date)
    return new_dates

import datetime

def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start must be a string")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    dates = []
    date_obj = datetime.datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        dates.append(date_obj)
        date_obj += datetime.timedelta(days=1)
    return dates

import csv
from collections import defaultdict
from typing import Dict

def fees_report(infile: str, outfile: str):
    # Read in the input data
    with open(infile, 'r', newline='') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    # Calculate late fees on a patron_id basis
    fees_by_patron = defaultdict(float)
    for row in data:
        if row['date_returned']:
            due_date = datetime.datetime.strptime(row['date_due'], '%m/%d/%Y')
            return_date = datetime.datetime.strptime(row['date_returned'], '%m/%d/%Y')
            if return_date > due_date:
                days_late = (return_date - due_date).days
                fee = 0.25 * days_late
                fees_by_patron[row['patron_id']] += fee

    # Write out a summary report for accounts with late fees only
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['patron_id', 'late_fees'])
        for patron_id, fees in fees_by_patron.items():
            if fees > 0:
                writer.writerow([patron_id, f'{fees:.2f}'])
