import os
print("\n\n=======================")
print("Django Configure Script")
print("=======================")

print("\nRunning this file will delete the Database and all the Migrations!")
print("Are you sure you want to continue[Y/n]?")
choice = input()
if(choice == 'n' or choice == 'N'):
  quit()

print("=======================")
print("   Deleting Database")
print("=======================")
os.system("rm -rf db.sqlite3")
print("+++++++Complete++++++++")

print("=======================")
print("  Deleting Migrations")
print("=======================")
os.system("rm -rf accounts/migrations/")
print("+++++++Complete++++++++")

print("=========================")
print("  Rebuilding Migrations")
print("=========================")
os.system("python manage.py makemigrations accounts")
os.system("python manage.py migrate")
print("+++++++Complete++++++++")

print("\nDo you want to create a Super User?[Y/n]")
choice = input()
if(choice == 'n' or choice == 'N'):
	quit()
os.system("python manage.py createsuperuser")

print("\n++++++++++++++++++")
print("  Running Server")
print("++++++++++++++++++\n")
os.system("python manage.py runserver")

