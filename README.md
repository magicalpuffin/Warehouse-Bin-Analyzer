# Warehouse Bin Analyzer
## Overview
Django web app for analyzing the optimal bin size for shipping orders. Uses PostgreSQL as the database.

# Django Notes
All must be in materialsite directory to access manage.py
## Running the App
- `py manage.py runserver`
## Migrations
Make migrations before applying them. If needed, just delete migrations with issues.
Can also migrate to zero to wipe database and recreate things
- `py manage.py makemigrations binanalyze`
- `py manage.py migrate binanalyze`
## Test
- `py manage.py shell`
- `py manage.py test binanalyze`