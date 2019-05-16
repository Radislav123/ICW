start all things from pickletax root(C:\ICW\pickletax)

run server:
..\ICW_venv\Scripts\python.exe manage.py runserver

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
1) delete migration files(without __init__.py and the folder)
2) delete database

to recover database:
make initial migration
