import csv
import datetime

def reformat_dates(dates):
    new_dates = []
    for date in dates:
        datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        new_date = datetime_obj.strftime('%d %b %Y')
        new_dates.append(new_date)
    return new_dates

def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start must be a string")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    dates = []
    date_obj = datetime.datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        dates.append(date_obj.strftime('%Y-%m-%d'))
        date_obj += datetime.timedelta(days=1)
    return dates

def add_date_range(values, start_date):
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))

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
            writer.writerow([patron_id, round(late_fee, 2)])
