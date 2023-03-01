#!/bin/bash
if [ ! "$1" ]
then
	echo "too short"
	exit 0
fi
curl localhost:1245/create_seats -X POST -H "Content-type: Application/json" -d '{"number_of_seats": '"$1"'}'
