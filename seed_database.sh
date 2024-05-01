#!/bin/bash

rm db.sqlite3
rm -rf ./otdjjangapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations otdjjangapi
python3 manage.py migrate otdjjangapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata brands
python3 manage.py loaddata types
python3 manage.py loaddata sizes
python3 manage.py loaddata articles
python3 manage.py loaddata userarticles
python3 manage.py loaddata outfits
python3 manage.py loaddata outfitarticles
python3 manage.py loaddata outfitphoto
