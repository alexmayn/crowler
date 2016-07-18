# crowler

The app showing how login to other site from yours app and downloading file from download folder.

It takes next params:

URL_INDEX = 'http://localhost:5000'       
URL_LOGIN = 'http://localhost:5000/login' 
URL_DOWNLOAD = 'http://localhost:5000/downloads/' 

LOG_FILE = 'sitelog.log' # file name to download

EXCLUDE_LINKS = ['http://localhost:5000/',
                 '/',
                 'EX.com',
                 '/admin/',
                 '/admin/logout/',
                 '/admin/useradd/,'
                 '/admin/create/']
                 
# Yours login and password to access the site:
login = '' 
password = ''

#Requirements
It using next libraries, you must install it first:
requests
urllib3
bs4

to install urllib you must install next packages on you linux:
zlib1g-dev libxml2 libxml2-dev libxslt-dev build-essential python-dev
