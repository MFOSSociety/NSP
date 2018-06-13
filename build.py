import os
os.system("python manage.py makemigrations accounts")
print("Makemigrations complete!")
os.system("python manage.py migrate")
print("Migration Complete")
os.system("python manage.py createsuperuser")
print("Running Server")
os.system("python manage.py runserver")

