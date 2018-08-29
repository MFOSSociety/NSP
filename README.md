# The Network Of Skilled People - NSP
<a href="https://travis-ci.com/NSP-Community/NSP"><img src="https://travis-ci.com/NSP-Community/NSP.svg?branch=master"></a>  <a href='https://coveralls.io/github/NSP-Community/NSP?branch=master'><img src='https://coveralls.io/repos/github/NSP-Community/NSP/badge.svg?branch=master' alt='Coverage Status' /></a>


Visit - http://thensp.pythonanywhere.com/

## Registration Page
![The Registration Page](https://i.imgur.com/S3qYQxv.jpg)

## Login Page
![The Login Page](https://i.imgur.com/lSky9uy.jpg)

## Home Page Part 1
![Home Page Part 1](https://i.imgur.com/IX9xsXz.jpg)

## Home Page Part 2
![Home Page Part 2](https://i.imgur.com/gQt5lho.jpg)

## Home Page Part 3
![Home Page Part 3](https://i.imgur.com/SFmL81J.jpg)

## Profile Page 
![The Profile Page](https://i.imgur.com/agKJpHR.jpg)

## Start Project Page
![Edit Profile Page](https://i.imgur.com/lmOrIwY.jpg)

## Change Password Page
![Change Password](https://i.imgur.com/CBat1bD.jpg)

## Installation Instructions (Linux/Unix)

##### Clone the repository and get inside NSP directory
```
git clone https://github.com/NSP-Community/NSP && cd NSP
```

##### Installing required Python3 libraries
```
sudo pip3 install -r requirements.txt
```

##### Make Migrations
```
python3 manage.py makemigrations accounts
python3 manage.py makemigrations notifications
python3 manage.py makemigrations nspmessage
python3 manage.py makemigrations project
python3 manage.py makemigrations issueSolution
```

##### Running the Server
```
python3 manage.py runserver
```

You should now be able to access NSP in localhost:8000 in your browser

### How to install NSP on your Windows System ?
Install Linux or buy a Mac and revisit https://github.com/NSP-Community/NSP/README.md

## Developers:
#### Backend Developers - <a href="https://github.com/rshrc">Rishi Banerjee</a> , <a href="https://github.com/pratikjain04">Pratik Jain</a> , <a href="https://github.com/gjergjk71">Gjergj Kadriu</a>
#### Frontend Developers - <a href="https://github.com/prachalgoyal03">Prachal Goyal</a>

