testTernaire README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- Rename development.ini.default to development.ini

- Update sqlalchemy.url in development.ini

- $VENV/bin/initialize_testTernaire_db development.ini

- $VENV/bin/pserve development.ini
