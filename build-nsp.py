import os, sys

# Custom Ubuntu Installation

# Installing of all the python packages and libraries
os.system("sudo pip3 install -r requirements.txt")

# Deleting Database even if it does not exist
os.system("rm -rf db.sqlite3")
print("Database db.sqlite3 removed...")

# Deleting all sort of Migrations
os.system("rm -rf accounts/migrations")
os.system("rm -rf nspmessage/migrations")
os.system("rm -rf project/migrations")
os.system("rm -rf notifications/migrations")
os.system("rm -rf issueSolution/migrations")
print("All Migrations Deleted...")

# Recreating all the migrations
os.system("python3 manage.py makemigrations")
os.system("python3 manage.py makemigrations accounts")
os.system("python3 manage.py makemigrations nspmessage")
os.system("python3 manage.py makemigrations project")
os.system("python3 manage.py makemigrations notifications")
os.system("python3 manage.py makemigrations issueSolution")

# Migrating Database
os.system("python3 manage.py migrate")
print("Migrations Regenerated...")

# Creating Superuser
os.system(
    "./manage.py shell -c \"from accounts.models import User; User.objects.create_superuser('admin@gmail.com', 'lemonjuice')\"")
print("\nCreated Superuser")

print("Super User Credentials")
print("Super User Email : admin@gmail.com")
print("Super User Password : lemonjuice")

# Creating 5 Custom Users
os.system(
    "./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='test1', email='test1@gmail.com', password='something')\"")
os.system(
    "./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='test2', email='test2@gmail.com', password='something')\"")
os.system(
    "./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='test3', email='test3@gmail.com', password='something')\"")
os.system(
    "./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='test4', email='test4@gmail.com', password='something')\"")
os.system(
    "./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='test5', email='test5@gmail.com', password='something')\"")

# TODO Creating 5 Custom Projects, Custom Issues, Notifications and working on other models

print("5 Random Users Created & 5 Random Projects Created")

print("Happy Manual Testing and Bug Hunting!")
os.system("python3 manage.py runserver")
