#!/usr/bin/python3
import csv
import datetime
from dateutil.relativedelta import relativedelta
import os


def process():
    with open('%s/sensor.csv' % os.getcwd(), 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='|')
        entries = []
        rownum = 0
        for row in rows:
            if rownum == 0:
                header = row
            elif rownum > 0:
                entry = {}
                colnum = 0
                for col in row:
                    entry[header[colnum]] = col.replace('"', '')
                    colnum += 1
                entries.append(entry)
            rownum += 1
    minutes_lis = []
    values_dict = {}
    for entry in entries:
        datetime_csv = entry.get('Datetime')
        date_aux = ''
        date = ''
        if datetime_csv:
            date_aux = datetime_csv.split(' ')[0].split('/')
        if date_aux and len(date_aux[2]) == 2:
            date = str(str(int(date_aux[2]) + 2000) + '-' + str(date_aux[1]) + '-' + date_aux[0])
            datetime_csv = date + ' ' + datetime_csv.split(' ')[1]
        else:
            date = str(date_aux[2]) + '-' + str(date_aux[1]) + '-' + str(date_aux[0])
            datetime_csv = date + ' ' + datetime_csv.split(' ')[1]
        first_date = datetime.datetime.strptime(datetime_csv, "%Y-%m-%d %H:%M")
        minutes_lis.append(first_date.time().strftime("%H:%M:%S"))
        next_date = first_date
        while next_date.date() == first_date.date():
            next_date += relativedelta(minutes=+10)
            if next_date.time().strftime("%H:%M:%S") in minutes_lis:
                break
            minutes_lis.append(next_date.time().strftime("%H:%M:%S"))
        values_dict.update({'Sensor': entry.get('Sensor'),
                            'Date': date})
        for minute in minutes_lis:
            values_dict.update({minute: entry.get('Measure')})
        with open('%s/output.csv' % os.getcwd(), 'wb') as csvfile:
            headder = ["Sensor", "Date"] + minutes_lis
            writer = csv.DictWriter(csvfile, fieldnames=headder)
            writer.writeheader()
            writer.writerow({x: values_dict.get(x) for x in headder})


if __name__ == "__main__":
    process()
