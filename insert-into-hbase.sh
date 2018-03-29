#!/bin/bash

# run N slave containers

if [ $# != 2  ]
then
	echo "Debe introducir los dos parametro de replicacion, el primero (F) seran las filas, el segundo (C) las columnas"
	exit 1
fi

python Test/replica_into_hbase.py $1 $2
