#!/bin/sh

echo "Populating Database"
echo "------ WARNING -------"
echo "Remove for Production"
python3 /usr/src/app/populate.py

echo "Starting API"
gunicorn --bind 0.0.0.0:8080 --workers 3 chintal.app:app
