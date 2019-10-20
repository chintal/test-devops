#!/bin/sh

echo "Populating Database"
python3 populate.py

echo "Starting API"
gunicorn --bind 0.0.0.0:8080 --workers 3 chintal.app:app
