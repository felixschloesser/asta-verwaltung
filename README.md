# key-management
A key management system written in django

## Database Setup
### macOS
`brew update`
`brew install mariadb`
`brew services start mariadb`

Access mariadb as root
`sudo mysql -u root`

`CREATE DATABASE keyManagement`
`CREATE USER 'django'@'localhost' IDENTIFIED BY '<password>';`
`GRANT ALL PRIVILEGES ON keyManagement.* TO 'django'@'localhost'`
`FLUSH PRIVILEGES;`

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



# Starting Django
`python manage.py runserver
