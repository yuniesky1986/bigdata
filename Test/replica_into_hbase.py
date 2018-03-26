#!/usr/bin/python3
import csv
import happybase
import os
import sys


def insert_row(batch, row_key, entry):
    batch.put(row_key, entry)


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
        print "Leyo el csv"
        families = {'SensorData': {}}
        cont = 1
        print c
        while cont <= c:
            families.update({"Measure%d" % cont: {}})
            cont += 1
        print families
        conn = happybase.Connection(host="172.17.0.2", port=7946)
        conn.open()
        conn.create_table('Sensores', families)
        print "Creo la tabla"
        table = conn.table('Sensores')
        batch = table.batch(batch_size=1000)
        print "Hizo el batch"
        for entry in entries:
            cont = 1
            while cont <= f:
                row_key = str(cont) + entry.get('Sensores')
                cont += 1
                insert_row(batch, row_key, entry)
            print "Inserto la primera fila"
            batch.send()
        conn.close()


if __name__ == "__main__":
    arg = sys.argv
    f = arg[1]
    c = arg[2]
    print f
    print c
    process(f, c)
