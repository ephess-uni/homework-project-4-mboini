from datetime import datetime, timedelta
from csv import DictReader, DictWriter

def reformat_dates(old_dates):
    new_dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%d %b %Y") for d in old_dates]
    return new_dates

def date_range(start, n):
    dates = [datetime.strptime(start, "%Y-%m-%d") + timedelta(days=i) for i in range(n)]
    return dates

def add_date_range(values, start_date):
    result = [(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i), v) for i, v in enumerate(values)]
    return result

def fees_report(infile, outfile):
    with open(infile) as f:
        rows = list(DictReader(f))
        data = []
        for row in rows:
            due_date = datetime.strptime(row['date_due'], "%m/%d/%Y")
            return_date = datetime.strptime(row['date_returned'], "%m/%d/%Y")
            days_late = (return_date - due_date).days
            if days_late > 0:
                late_fees = round(days_late * 0.25, 2)
            else:
                late_fees = 0.0
            data.append({'patron_id': row['patron_id'], 'late_fees': late_fees})
        grouped_data = {}
        for item in data:
            grouped_data[item['patron_id']] = grouped_data.get(item['patron_id'], 0) + item['late_fees']
        output_data = [{'patron_id': k, 'late_fees': round(v, 2)} for k, v in grouped_data.items()]
    with open(outfile, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(output_data)

if __name__ == '__main__':
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path
    book_returns_path = get_data_file_path('book_returns_short.csv')
    outfile = 'book_fees.csv'
    fees_report(book_returns_path, outfile)
    with open(outfile) as f:
        print(f.read())
