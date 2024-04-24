#!/bin/bash

rm db.sqlite3
rm -rf ./otdjjangapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations otdjjangapi
python3 manage.py migrate otdjjangapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

