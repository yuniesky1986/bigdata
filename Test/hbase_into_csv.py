#!/usr/bin/python3
import csv
import happybase
import os
import sys


def process(f, c):
    with open('%s/end.csv' % os.getcwd(), 'wb') as csvfile:
        conn = happybase.Connection(host="172.17.0.2", port=7946)
        conn.open()
        table = conn.table('Sensores')
        values = {}
        row_key = ''
        for key, data in table.scan(row_start=f, columns=['SensorData', "Measure%d" % c]):
            row_key = key
            values = data
            break
        headder = ['Key'] + [x for x in values.iterkeys()]
        writer = csv.DictWriter(csvfile, fieldnames=headder)
        writer.writeheader()
        write_dict = {'Key': row_key}.update({x: values.get(x) for x in headder})
        writer.writerow(write_dict)
        conn.close()


if __name__ == "__main__":
    arg = sys.argv
    f = arg[1]
    c = arg[2]
    process(f, c)
