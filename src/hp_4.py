# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
from typing import List, Tuple


def reformat_dates(dates):
    new_dates = []
    for date_str in dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = datetime.strftime(date_obj, '%d %b %Y')
        new_dates.append(new_date_str)
    return new_dates


def date_range(date_str, n):
    start = datetime.strptime(date_str, '%Y-%m-%d')
    dates = [start + timedelta(days=i) for i in range(n)]
    return dates

input_str = input("Enter start date and number of days (e.g. '2000-01-01,3'): ")
date_str, n = input_str.split(',')
dates = date_range(date_str, int(n))
print(dates)


def date_range(start: str, n: int) -> List[datetime]:
    if not isinstance(start, str):
        raise TypeError("start date must be a string in yyyy-mm-dd format")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    return [datetime.strptime(start, "%Y-%m-%d") + timedelta(days=i) for i in range(n)]

def add_date_range(values: List[float], start_date: str) -> List[Tuple[datetime, float]]:
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    if not isinstance(start_date, str):
        raise TypeError("start_date must be a string in yyyy-mm-dd format")
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))
    
values = input("Enter a list of values separated by commas: ")
values = [float(val.strip()) for val in values.split(",")]
start_date = input("Enter the start date in yyyy-mm-dd format: ")
result = add_date_range(values, start_date)
print(result)


import csv

def fees_report(infile, outfile):
    # Read in the CSV file
    with open(infile, 'r') as f:
        reader = csv.DictReader(f)
        # Create a dictionary to store late fees by patron_id
        late_fees = {}
        for row in reader:
            patron_id = row['patron_id']
            due_date = row['due_date']
            return_date = row['return_date']
            # Check if the book was returned late
            if return_date > due_date:
                # Calculate the number of days late
                days_late = (datetime.strptime(return_date, '%Y-%m-%d') - datetime.strptime(due_date, '%Y-%m-%d')).days
                # Calculate the late fee
                late_fee = days_late * 0.25
                # Add the late fee to the patron's account
                if patron_id in late_fees:
                    late_fees[patron_id] += late_fee
                else:
                    late_fees[patron_id] = late_fee
    # Write out the summary report for accounts with late fees
    with open(outfile, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['patron_id', 'late_fee'])
        for patron_id, fee in late_fees.items():
            if fee > 0:
                writer.writerow([patron_id, fee])

## fees_report()
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
            due_date = datetime.strptime(row['date_due'], '%m/%d/%y')
            return_date = datetime.strptime(row['date_returned'], '%m/%d/%y')
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

