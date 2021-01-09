# key-management
A key management system written in django

## Database Setup
### macOS
`brew update`
`brew install postgres`
`brew services start postgres`

Access the postgres command line as root
`sudo mysql -u root`

`CREATE DATABASE astadb`
`CREATE USER django WITH PASSWORD 'changeme'`
`GRANT ALL PRIVILEGES ON astadb TO django'`

`ALTER ROLE django SET client_encoding TO 'utf8';`
`ALTER ROLE django SET default_transaction_isolation TO 'read committed';`
`ALTER ROLE django SET timezone TO 'Europe/Berlin';`:

### ubuntu
`sudo apt update`
`sudo apt install mariadb-server`
`sudo mysql_secure_installation`

`sudo apt install libmariadbclient-dev`

## Virtualenv
`brew update`
`brew upgrade python3`

`python3 -m pip install --upgrade pip`

`python3 -m venv .django-env`
`source .django-env/bin/activate`

`pip install -r requirements.txt`



## Starting Django
`python manage.py runserver
