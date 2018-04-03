#!/usr/bin/python3
import csv
import happybase
import os
import sys
import datetime
from dateutil.relativedelta import relativedelta


def process(f, c):
    with open('%s/end.csv' % os.getcwd(), 'wb') as csvfile:
        conn = happybase.Connection(host="master.krejcmat.com", port=9090)
        conn.open()
        table = conn.table('Sensores')
        print "Conexion a hbase realizada"
        values = {}
        row_key = ''
        for key, data in table.scan(row_start=str(f)):
            row_key = key
            values = data
            break
        families = ['SensorData', "Measure%d" % c]
        headder = ["Sensor", "Date"]
        first_date = datetime.datetime.strptime(values.get("%s:%s" %(families[0], headder[1])), "%Y-%m-%d")
        minutes_lis = [first_date.time().strftime("%H:%M:%S")]
        next_date = first_date
        while next_date.date() == first_date.date():
            next_date += relativedelta(minutes=+10)
            if next_date.time().strftime("%H:%M:%S") in minutes_lis:
                break
            minutes_lis.append(next_date.time().strftime("%H:%M:%S"))
        writer = csv.DictWriter(csvfile, fieldnames=headder + minutes_lis)
        print "Escribiendo las cabeceras en el csv"
        writer.writeheader()
        write_dict = {x: values.get("%s:%s" % (families[0], x)) for x in headder}
        write_dict[headder[0]] = str(f) + write_dict[headder[0]]
        write_dict.update({x: values.get("%s:%s" % (families[1], x)) for x in minutes_lis})
        print "Escribiendo los valores en el csv" 
        writer.writerow(write_dict)
        conn.close()


if __name__ == "__main__":
    arg = sys.argv
    f = arg[1]
    c = arg[2]
    print "Obteniendo medidor %s de la columna %c" % (f,c)
    process(int(f), int(c))
