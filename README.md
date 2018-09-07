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
### Small procedure


##### Clone the repository and get inside NSP directory
```
git clone https://github.com/NSP-Community/NSP && cd NSP && chmod +x go.sh
```

##### Now run the bash script
```
./go.sh
```
> **NOTE** : This will create a virtualenv named "mason" by default. Always move in virtualenv before starting any dev process or testing process! 
>> In order to move in virtualenv shell execute `source mason/bin/activate`
***
### Long procedure

##### Clone the repository and get inside NSP directory
```
git clone https://github.com/NSP-Community/NSP && cd NSP
```

##### (Optional) Only if you need virtual environment
```
sudo apt-get update
sudo apt-get install virtualenv
virtualenv example_name --python=python3
source example_name/bin/activate
```

##### Installing required Python3 libraries
```
sudo python3 -m pip install -r requirements.txt
```

##### Make Migrations
```
python3 manage.py makemigrations accounts
python3 manage.py makemigrations notifications
python3 manage.py makemigrations nspmessage
python3 manage.py makemigrations project
python3 manage.py makemigrations issueSolution
python3 manage.py migrate
```

##### Running the Server
```
python3 manage.py runserver
```

You should now be able to access NSP in localhost:8000 in your browser
***
### How to install NSP on your Windows System ?
You can install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) on Windows 10 and we suggest you to go for Ubuntu! After this the installation process is same as any other linux distro 

## Developers:
#### Backend Developers - <a href="https://github.com/rshrc">Rishi Banerjee</a> , <a href="https://github.com/pratikjain04">Pratik Jain</a> , <a href="https://github.com/gjergjk71">Gjergj Kadriu</a>
#### Frontend Developers - <a href="https://github.com/prachalgoyal03">Prachal Goyal</a>

