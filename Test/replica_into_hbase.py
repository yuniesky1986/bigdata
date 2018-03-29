#!/usr/bin/python3
import csv
import happybase
import os
import sys


def process(f, c):
    with open('%s/output.csv' % os.getcwd(), 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='|')
        entries = []
        rownum = 0
        header = []
        for row in rows:
            if rownum == 0:
                header.extend(row)
            elif rownum > 0:
                entry = {}
                colnum = 0
                for col in row:
                    entry[header[colnum]] = col.replace('"', '')
                    colnum += 1
                entries.append(entry)
            rownum += 1
        families = {'SensorData': {}}
        cont = 1
        while cont <= c:
            families.update({"Measure%d" % cont: {}})
            cont += 1
        conn = happybase.Connection(host="master.krejcmat.com", port=9090)
        conn.open()
        tables = conn.tables()
        if "Sensores" in tables:
            table = conn.table('Sensores')
        else:
            conn.create_table('Sensores', families)
            table = conn.table('Sensores')
        batch = table.batch(batch_size=1000)
        for entry in entries:
            for family in families.iterkeys():
                if family == "SensorData":
                    for head in header[:2]:
                        cont = 1
                        while cont <= f:
                            row_key = str(cont) + entry.get('Sensor')
                            cont += 1
                            batch.put(row_key, {'%s:%s' % (family, head): entry[head]})
                else:
                    for head in header[2:]:
                        cont = 1
                        while cont <= f:
                            row_key = str(cont) + entry.get('Sensor')
                            cont += 1
                            batch.put(row_key, {'%s:%s' % (family, head): entry[head]})
            batch.send()
        conn.close()


if __name__ == "__main__":
    arg = sys.argv
    f = arg[1]
    c = arg[2]
    process(int(f), int(c))
