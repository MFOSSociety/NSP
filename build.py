import os
print("Running this file will delete the Database and all the Migrations!")
print("Are you sure you want to continue[Y/n]?")
choice = input()
if(choice == 'n' or choice == 'N'):
  quit()
print("Deleting Database")
os.system("rm -rf db.sqlite3")
print("Deleting Migrations Folder...")
os.system("rm -rf accounts/migrations/")
print("Rebuilding the Migrations...")
os.system("python manage.py makemigrations accounts")
os.system("python manage.py migrate")
print("Migration Complete.. Database 'db.sqlite' created")
print("Create a Super User")
os.system("python manage.py createsuperuser")
print("Running Server")
os.system("python manage.py runserver")

