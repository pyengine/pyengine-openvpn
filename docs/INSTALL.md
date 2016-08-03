# Pyengine

## Intall OpenVPN package(Recommended)

You can install OpenVPN automatically, using jeju -m openvpn.md

## Prerequisite

Keyword | Value     | Description
----    | ----      | ----
PROJECT | pyengine-openvpn | Project name
 
# Installation

## Install libraries

Pyengine is based on apache and python django framework

~~~bash
apt-get update
export DEBIAN_FRONTEND=noninteractive
apt-get install -y git python-dev python-pip mariadb-server apache2 libapache2-mod-wsgi python-mysqldb libyaml-cpp-dev libyaml-dev
~~~

## Install PIP libraries for django

~~~bash
pip install django
pip install django-log-request-id
pip install dicttoxml
pip install xmltodict
pip install routes
pip install rsa
pip install pytz
pip install pyyaml
pip install django-cors-headers
~~~

## Download source

Download pyengine source

~~~bash
cd /opt/
git clone https://github.com/pyengine/pyengine.git ${PROJECT}
~~~

## Update python module path environment

edit /usr/local/lib/python2.7/site-packages/pyengine.pth

~~~text
/opt/${PROJECT}
~~~

# Update Configuration

## Update Apache configuration

edit /etc/apache2/sites-available/pyengine.conf

~~~text
<VirtualHost *:80>
    Alias /dashboard    /opt/${PROJECT}/dashboard
    <Directory /opt/${PROJECT}/dashboard>
        Require all granted
    </Directory>

    Alias /static    /opt/${PROJECT}/static
    <Directory /opt/${PROJECT}/static>
        Require all granted
    </Directory>

    WSGIScriptAlias / /opt/${PROJECT}/pyengine/wsgi.py
    WSGIPassAuthorization On

    <Directory /opt/${PROJECT}/pyengine>
    <Files wsgi.py>
        Require all granted
    </Files>
    </Directory>

    AddDefaultCharset UTF-8
</VirtualHost>
~~~

Enable the pyengine

~~~bash
a2dissite default
a2ensite pyengine
~~~

# Create Database

Create pyengine database

~~~expect
spawn mysql -u root -e "create database pyengine character set utf8 collate utf8_general_ci"
expect "Enter password: "
send "\n";
interact
~~~

## Update global.conf

edit /var/pyengine-openvpn/pyengine/conf/global.conf

~~~text
GLOBAL: 
    # Auth Settings
    # API Auth Type : noauth | xauth
    AUTH_TYPE: xauth
    AUTH_HOST: localhost
    AUTH_URL: '/api/v1/token/auth'

    NO_AUTH_MODULES:
        - token

    SYSTEM_KEY: 816801afffe508cf99cb
    SYSTEM_AUTH_MODULES:
        - system

    # Default Settings
    DEFAULT_LANGUAGE: ko
    DEFAULT_TIMEZONE: Asia/Seoul
    DEFAULT_JOB_TIMEOUT: 1800
    TOKEN_EXPIRE_TIME: 86400
    DATETIME_FIELDS: 
        - created
        - last_update
        - finished
        - deleted
    SERVER_ADDRESS: ${IP}
~~~

## Update django DB

~~~bash
mkdir /var/log/pyengine
chown -R www-data:www-data /var/log/pyengine

cd /opt/${PROJECT}
python manage.py makemigrations
python manage.py migrate
~~~

## Update OpenVPN script

edit /etc/openvpn/easy-rsa/pyengine-build.key.sh

~~~text
#! /bin/bash

cd /etc/openvpn/easy-rsa
source ./vars

export KEY_EMAIL=$2
export KEY_OU=$3

./build-key --batch $1
~~~

update permission 

~~~bash
chmod 755 /etc/openvpn/easy-rsa/pyengine-build-key.sh
echo "www-data ALL=(/etc/openvpn/easy-rsa/pyengine-build-key.sh) NOPASSWD: ALL" > /etc/sudoers
~~~

## Update static directory for key save

~~~bash
mkdir /opt/${REPO}/static/keys
chown -R www-data:www-data /opt/${REPO}/static/keys
# Restart Apache

~~~bash
service apache2 restart
~~~


