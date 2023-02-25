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

import datetime

def add_date_range(values, start_date):
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))

import csv
import datetime

def fees_report(infile, outfile):
    with open(infile, 'r') as fin, open(outfile, 'w', newline='') as fout:
        reader = csv.DictReader(fin)
        writer = csv.writer(fout)
        writer.writerow(['patron_id', 'late_fees'])
        late_fees = {}
        for row in reader:
            patron_id = row['patron_id']
            date_due = datetime.datetime.strptime(row['date_due'], '%Y-%m-%d')
            date_returned = datetime.datetime.strptime(row['date_returned'], '%Y-%m-%d')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = days_late * 0.25
                if patron_id in late_fees:
                    late_fees[patron_id] += late_fee
                else:
                    late_fees[patron_id] = late_fee
        for patron_id, late_fee in late_fees.items():
            writer.writerow([patron_id, late_fee])

import datetime
import csv
import pytest

@pytest.fixture
def book_returns_short():
    data = [
        {'patron_id': '001', 'date_due': '2022-01-01', 'date_returned': '2022-01-05'},
        {'patron_id': '002', 'date_due': '2022-01-02', 'date_returned': '2022-01-06'},
        {'patron_id': '003', 'date_due': '2022-01-03', 'date_returned': '2022-01-05'},
        {'patron_id': '004', 'date_due': '2022-01-04', 'date_returned': '2022-01-05'},
        {'patron_id': '005', 'date_due': '2022-01-05', 'date_returned': '2022-01-05'},
    ]
    with open('book_returns_short.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['patron_id', 'date_due', 'date_returned'])
        writer.writeheader()
        writer.writerows(data)
    yield 'book_returns_short.csv'
    os.remove('book_returns_short.csv')

@pytest.fixture
def book_returns():
    data = [
        {'patron_id': '001', 'date_due': '2022-01-01', 'date_returned': '2022-01-05'},
        {'patron_id': '002', 'date_due': '2022-01-02', 'date_returned': '2022-01-06'},
        {'patron_id': '003', 'date_due': '2022-01-03', 'date_returned': '2022-01-05'},
        {'patron_id': '004', 'date_due': '2022-01-04', 'date_returned': '2022-01-05'},
        {'patron_id': '005', 'date_due': '2022-01-05', 'date_returned': '2022-01-05'},
        {'patron_id': '006', 'date_due': '2022-01-06', 'date_returned': '2022-01-07'},
        {'patron_id': '007', 'date_due': '2022-01-07', 'date_returned': '2022-01-08'},
        {'patron_id': '008', 'date_due': '2022-01-08', 'date_returned': '2022-01-09'},
        {'patron_id': '009', 'date_due': '2022-01-09', 'date_returned': '2022-01-10'},
        {'patron_id': '010', 'date_due': '2022-01-10', 'date_returned': '2022-01-11'},
    ]
    with open('book_returns.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['patron_id', 'date_due',
