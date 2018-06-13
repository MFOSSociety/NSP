echo "=======================";
echo "Django Configure Script";
echo "=======================";
echo "";
echo "Deleting Database";
rm -rf db.sqlite3
echo "Deleting Migrations"
rm -rf accounts/migrations
echo "Migrating..."
python manage.py makemigrations accounts
echo "Constructing Database..."
python manage.py migrate
echo "Starting Server..."
python manage.py runserver
