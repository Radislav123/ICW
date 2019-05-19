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
exec(open('databasedaemon\\databasefilling\\fill_database_by_basics.py', encoding = 'utf-8').read())

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
http://ec2-18-225-6-37.us-east-2.compute.amazonaws.com:8001/pickletax/databasedaemon/
authorization:
http://ec2-18-225-6-37.us-east-2.compute.amazonaws.com:8001/pickletax/databasedaemon/authorization/
status update:
http://ec2-18-225-6-37.us-east-2.compute.amazonaws.com:8001/pickletax/databasedaemon/userstatusupdate/
status change:
http://ec2-18-225-6-37.us-east-2.compute.amazonaws.com:8001/pickletax/databasedaemon/statuschange/

http status codes in use:
	authorization_ok = 200
	authorization_not_ok = 400
	verification_ok = 200
	verification_not_ok = 400
	update_ok = 200
	unexpected_server_error = 500

http status codes:
HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS

HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
HTTP_207_MULTI_STATUS

HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED
HTTP_307_TEMPORARY_REDIRECT

HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_REQUEST_ENTITY_TOO_LARGE
HTTP_414_REQUEST_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_507_INSUFFICIENT_STORAGE
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED