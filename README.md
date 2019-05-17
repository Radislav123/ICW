start all things from pickletax root(C:\ICW\pickletax)

run server locally:
..\ICW_venv\Scripts\python.exe manage.py runserver

run server reachable from the Internet:
python manage.py runserver ec2-18-218-255-8.us-east-2.compute.amazonaws.com:9090

run django shell:
..\ICW_venv\Scripts\python.exe manage.py shell

run a script in django shell:
exec(open('path\\to\\a\\script\\from\\pickletax\\root\\script.py', encoding = 'utf-8').read())
example:
exec(open('databasedaemon\\fill_database_by_basics.py', encoding = 'utf-8').read())

exit shell:
exit()

database migrations:
..\ICW_venv\Scripts\python.exe manage.py makemigrations
..\ICW_venv\Scripts\python.exe manage.py migrate

to drop database:
delete migration files(without __init__.py and the folder)
delete database

to recover database:
make initial migration

URLs:
Hello, world:
http://ec2-3-16-24-20.us-east-2.compute.amazonaws.com:9090/pickletax/databasedaemon/
authorization:
http://ec2-3-16-24-20.us-east-2.compute.amazonaws.com:9090/pickletax/databasedaemon/authorization/