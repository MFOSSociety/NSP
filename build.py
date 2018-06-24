import os
import sys

# runserver function
def runserver():
	print(colored("=======================", "green"))
	print(colored("  Running Server", "yellow"))
	print(colored("=======================", "green"))
	os.system("python3 manage.py runserver")

if('termcolor' not in sys.modules):
	os.system("sudo pip3 install termcolor")

	
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
os.system("python3 manage.py makemigrations accounts")
os.system("python3 manage.py migrate")
print(colored("+++++++Complete++++++++", "green"))

os.system("./manage.py shell -c \"from accounts.models import User; User.objects.create_superuser('admin@gmail.com', 'something')\"")
print("\nCreated Superuser")
print(colored("\nCreating Starting Users", "yellow"))
os.system("./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='rshrc1', email='rshrc404@gmail.com', password='something')\"")
os.system("./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='lol', email='lol404@gmail.com', password='something')\"")
os.system("./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='lmao', email='lmao@gmail.com', password='something')\"")
os.system("./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='shrek', email='shrek@gmail.com', password='something')\"")
os.system("./manage.py shell -c \"from accounts.models import User; User.objects._create_user(username='neo', email='neo@gmail.com', password='something')\"")
print(colored("Created 5 Users", "yellow"))

print(colored("\nCreating 5 Random Projects", "yellow"))
os.system("./manage.py shell -c \"from accounts.models import ProjectDetail; ProjectDetail.objects.create(project_name='DeepML', mentor_name='Rishi Banerjee', paid=True, description='Deep Learning Program', start_date='1999-09-01', branch='CSE/IT')\"")
os.system("./manage.py shell -c \"from accounts.models import ProjectDetail; ProjectDetail.objects.create(project_name='Disaster Drone', mentor_name='Pratik Jain', paid=True, description='Disaster Helper', start_date='1999-09-01', branch='CSE/IT')\"")
os.system("./manage.py shell -c \"from accounts.models import ProjectDetail; ProjectDetail.objects.create(project_name='Azure', mentor_name='Kshitij Gupta', paid=True, description='Server Launch', start_date='1999-09-01', branch='CSE/IT')\"")
os.system("./manage.py shell -c \"from accounts.models import ProjectDetail; ProjectDetail.objects.create(project_name='DeepAI', mentor_name='Tushar Saddana', paid=True, description='AI for Application', start_date='1999-09-01', branch='CSE/IT')\"")
os.system("./manage.py shell -c \"from accounts.models import ProjectDetail; ProjectDetail.objects.create(project_name='WebAndApp', mentor_name='Vidyanshu Jain', paid=True, description='Weba and App for Elicit', start_date='1999-09-01', branch='CSE/IT')\"")
os.system("./manage.py shell -c \"from accounts.models import ProjectDetail; ProjectDetail.objects.create(project_name='InfoMUJ', mentor_name='Ashish Kumar', paid=True, description='New Guidance App for MUJ', start_date='1999-09-01', branch='CSE/IT')\"")

print(colored("Created 5 Random Projects", "yellow"))

print("\nNow you can start testing the NSP Application :)")


print(colored("\nRunning Server\n\n", "green"))


os.system("python3 manage.py runserver")

# Scripted with love by Rishi Banerjee




