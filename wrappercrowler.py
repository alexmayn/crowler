from crowler import Requester
from bs4 import BeautifulSoup
from config import *



# create object requester
requester = Requester()

# Get available forms
forms = requester.get_forms(URL_LOGIN)

# First We Login on the site
requester.submit(forms[0], {'username': login,
                            'password': password
                            })

# Then collect list links on main page
response = requester.open(URL_INDEX)

print '\n', requester.get_cookies() # show cookies
print '\n', requester.get_headers() # show headers

# Parse the response text
html = BeautifulSoup(response.text, 'lxml')

# Show metategs
for meta in html.find_all('meta'):
    print meta.get('content')

list_disallow = EXCLUDE_LINKS
list_links = []
# Searche STATISTICS-pages
for link in html.find_all('a'):
    if not link.get('href') in EXCLUDE_LINKS:
        list_links.append(link.get('href'))

if list_links:
    stats = requester.searche_stats(URL_INDEX, list_links, list_disallow)


# Searche STATISTICS-pages searche_stats(self, base_url, links, statistics):
for stat in stats:
    print stat['text']





#print html.getText() #show text of main page

# Request to log file
response = requester.open(URL_DOWNLOAD + LOG_FILE)

# Save file in stream with chanks
with open(LOG_FILE, 'wb') as out_stream:
    for chunk in response.iter_content(1024):
        out_stream.write(chunk)


