import os
import sys

# runserver function
def runserver():
	print(colored("=======================", "green"))
	print(colored("  Running Server", "yellow"))
	print(colored("=======================", "green"))
	os.system("python manage.py runserver")

if('termcolor' not in sys.modules):
	os.system("sudo pip install termcolor")

	
from termcolor import colored
print(colored("\n\n=======================", "green"))
print(colored("Django Configure Script", "yellow"))
print(colored("=======================", "green"))

print(colored("\nRunning this file will delete the Database and all the Migrations!", "red"))
print(colored("Are you sure you want to continue[Y/n]?", "magenta"))
choice = input()
if(choice == 'n' or choice == 'N'):
  runserver()

print(colored("=======================", "green"))
print(colored("   Deleting Database", "yellow"))
print(colored("=======================", "green"))
os.system("rm -rf db.sqlite3")
print(colored("+++++++Complete++++++++", "green"))


print(colored("=======================", "green"))
print(colored("  Deleting Migrations", "yellow"))
print(colored("=======================", "green"))
os.system("rm -rf accounts/migrations/")
print(colored("+++++++Complete++++++++", "green"))

print(colored("=========================", "green"))
print(colored("  Rebuilding Migrations", "yellow"))
print(colored("=========================", "green"))
os.system("python manage.py makemigrations accounts")
os.system("python manage.py migrate")
print(colored("+++++++Complete++++++++", "green"))

print(colored("\nDo you want to create a Super User?[Y/n]", "blue"))
choice = input()
if(choice == 'n' or choice == 'N'):
	runserver()
os.system("python manage.py createsuperuser")

