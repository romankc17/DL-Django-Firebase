from requests.adapters import HTTPAdapter
from urllib3 import Retry
import time
import requests

# to disable insecure request warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {"Connection": "keep-alive",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])


def waitForResourceAvailable(session, request_method, url, **kwargs):
    session.headers.update(headers)

    while True:
        try:
            session.mount(url, HTTPAdapter(max_retries=retries))
            if request_method == 'get':
                response = session.get(url, verify=False)

            elif request_method == 'post':
                response = session.post(url, data=kwargs['params'], verify=False)
            return response
        except:
            print('Sleeping')
            time.sleep(2)


def waitforResponse(cookies, request_method, url, **kwargs):
    with requests.session() as c:
        c.cookies.update(cookies)
        c.headers.update(headers)

        while True:
            try:
                c.mount(url, HTTPAdapter(max_retries=retries))
                if request_method == 'get':
                    response = c.get(url, cookies=cookies, verify=False)

                elif request_method == 'post':
                    response = c.post(url, data=kwargs['params'], cookies=cookies, verify=False)
                return response



            except:
                print('Sleeping')
                time.sleep(2)

