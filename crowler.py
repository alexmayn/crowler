import json
import requests
import urlparse
from bs4 import BeautifulSoup
from config import *

class Requester(object):
    def __init__(self, headers=None, cookies=None):
        if cookies is None:
            cookies = {}
        if headers is None:
            headers = {}
        self.session = requests.session()

        headers.update({
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
        })

        self.session.headers.update(headers)
        self.add_to_cookies(cookies)

    def open(self, url):
        return self._get(url)

    def submit(self, form, data=None, headers=None, method=None):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        data = self._merge(form.data, data)

        if method == 'get' or form.type == 'get':
            return self._get(form.url, data, headers)
        else:
            return self._post(form.url, data, headers)

    def get_forms(self, url):
        response = self._get(url)

        # update the url in case we were redirected
        url = response.url

        html = BeautifulSoup(response.text, 'lxml')
        forms = []
        for form in html.find_all('form'):
            inputs = []
            for _input in form.find_all('input'):
                inputs.append({
                    'name': _input['name'] if 'name' in _input.attrs else '',
                    'value': _input['value'] if 'value' in _input.attrs else '',
                    'type': _input['type'] if 'type' in _input.attrs else ''
                })

            method = form['method'].lower() if 'method' in form.attrs else 'get'
            forms.append(LoginForm(url, form['action'], inputs, method))

        return forms

    # return dictionary of cookies
    def get_cookies(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    # dictionary to add/overwrite cookies
    def add_to_cookies(self, cookie):
        self.session.cookies = requests.utils.cookiejar_from_dict(self._merge(self.get_cookies(), cookie))

    # return dictionary of headers
    def get_headers(self):
        return dict(self.session.headers)

    # dictionary to add/overwrite headers
    def add_to_headers(self, header):
        self.session.headers = self._merge(self.session.headers, header)

    def _request(self, method, url, params=None, headers=None, cookies=None):
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        if params is None:
            params = {}
        headers = self._merge(self.session.headers, headers)

        cookies = self._merge(self.get_cookies(), cookies)
        if method == 'get':
            return self.session.request(method.upper(), url, params=params, headers=headers, cookies=cookies)
        else:
            return self.session.request(method.upper(), url, data=params, headers=headers, cookies=cookies)

    def _get(self, url, *arg):
        return self._request('get', url, *arg)

    def _post(self, url, *arg):
        return self._request('post', url, *arg)

    def _merge(self, dict1, dict2):
        return dict(dict1.items() + dict2.items())

    def searche_stats(self, base_url, list_links, list_disallow, statistics=[]):
            """
            Method to recursion get all links and searche all statistics tegs <td></td>

            :param links: list of lonks
            :type links: dict
            :param base_url: index url
            :type base_url: str
            :param statistics: text in html with table statistics
            :type statistics: str
            :param list_disallow: list of urls for exclude on nex iteration of recursion
            :type list_disallow: dict
            """
            #<table  class="table table-bordered table-striped" id="statistics">

            #print soup.find('div', id='top_menu')

            # open page
            for link in list_links:
                # link-list is not
                if not link.startswith('/'):
                    #link = list_links
                    continue

                list_disallow = list_disallow + list_links

                # check link in exclude list
                repl_str = (base_url+link).replace('/admin/','/')

                if repl_str.find('/clearstats',0,len(repl_str)) != -1:
                    if not repl_str in EXCLUDE_LINKS:
                        EXCLUDE_LINKS.append(repl_str)

                if not repl_str in EXCLUDE_LINKS and repl_str != (base_url+'/'):

                    response = self.open(repl_str)

                    # Find tables with statistics-id
                    html_table = BeautifulSoup(response.text, 'lxml')
                    find_stats =  html_table.find('table', id='statistics')

                    if find_stats:
                        statistics.append( {'text': 'Page stats: '+repl_str} )
                        statistics.append( {'text': find_stats.text} )

                    # Find next links
                    list_in = []
                    html_links = BeautifulSoup(response.text, 'lxml')
                    for link_in in html_links.find_all('a'):
                       if not link_in.find(0,len(link), '/') == 0:
                           if not link_in.get('href')  in EXCLUDE_LINKS and link_in.get('href') != link:
                               if link_in.get('href') in list_disallow:
                                   continue
                               list_in.append(link_in.get('href'))

                    list_new = []
                    for link_in in list_in:
                        if link_in in list_new:
                            continue
                        list_new.append(link_in)

                    list_in = list_new

                    if list_in:
                        statistics = statistics + self.searche_stats(base_url, list_in, list_disallow, [])

            return statistics


class LoginForm(object):
    def __init__(self, url, action, inputs, ftype):
        self.url = urlparse.urljoin(url, action)
        self.data = {}

        for _input in inputs:
            if _input['name'] is not '':
                self.data[_input['name']] = _input['value']

        if ftype != 'get' and ftype != 'post':
            raise Exception('Form type invalid: \'%s\'')

        self.type = ftype

    def __str__(self):
        return json.dumps({
            'url': self.url,
            'data': self.data,
            'type': self.type
        })
