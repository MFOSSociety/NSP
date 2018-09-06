#!/bin/bash
echo -e "\e[32m[!] Cleaning mess...\e[0m"
rm -rf db.sqlite3 >/dev/null 2>&1
find . -not -path "./mason/*" -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -not -path "./mason/*" -path "*/migrations/*.pyc"  -delete
echo -e "\e[32m[+] Updating the system!\e[0m"
sudo apt-get update >/dev/null 2>&1
echo -e "\e[32m[+] Installing python3 and virtualenv!\e[0m"
sudo apt-get install virtualenv python3 >/dev/null 2>&1
echo -e "\e[32m[+] Making a venv!\e[0m"
virtualenv mason --python=python3 >/dev/null 2>&1
echo -e "\e[32m[+] Shifting to venv!\e[0m"
source ./mason/bin/activate >/dev/null 2>&1
echo -e "\e[32m[+] Installing requirements!\e[0m"
./mason/bin/python3 -m pip install -r requirements.txt >/dev/null 2>&1
echo -e "\e[32m[+] Making migrations!\e[0m"
./mason/bin/python3 manage.py makemigrations >/dev/null 2>&1
./mason/bin/python3 manage.py makemigrations accounts >/dev/null 2>&1
./mason/bin/python3 manage.py makemigrations notifications >/dev/null 2>&1
./mason/bin/python3 manage.py makemigrations masonmessage >/dev/null 2>&1
./mason/bin/python3 manage.py makemigrations project >/dev/null 2>&1
./mason/bin/python3 manage.py makemigrations issueSolution >/dev/null 2>&1
./mason/bin/python3 manage.py migrate >/dev/null 2>&1
echo -e "\e[31m[!] Make a superuser!\e[0m"
./mason/bin/python3 manage.py createsuperuser
echo -e "\e[31m[+] Firing up the server!\e[0m"
echo -e "\e[31m[!] Click here to access : http://127.0.0.1:8000/ \e[0m"
./mason/bin/python3 manage.py runserver >/dev/null 2>&1
