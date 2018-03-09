#!/bin/bash 

rm -rf db/ migrations/
mkdir db

if [ $? -eq 0 ]
then
   python manage.py db init
else
   exit 1
fi

if [ $? -eq 0 ]
then
   python manage.py db migrate -m "initial migration"
else
   exit 1
fi

if [ $? -eq 0 ]
then
   python manage.py db upgrade
else
   exit 1
fi

if [ $? -eq 0 ]
then
   python  manage.py init_data
else
   exit 1
fi


