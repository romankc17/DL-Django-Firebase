import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import time
import requests

# to disable insecure request warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {"Connection": "keep-alive",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
retries = Retry(total=20,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504],
                other=100)


def waitForResourceAvailable(session, request_method, url, **kwargs):
    # session.headers.update(headers)
    while True:
        try:
            session.mount(url, HTTPAdapter(max_retries=retries))
            if request_method == 'get':
                response = session.get(url,headers=headers,verify=False)

            elif request_method == 'post':
                response = session.post(url, data=kwargs['params'],headers=headers,verify=False )
            return response
        except Exception as ec:
            print(ec)


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

home_url='https://onlineedlreg.dotm.gov.np/dlNewRegHome'
next_url='http://onlineedlreg.dotm.gov.np/newDlApplicationEntry_.action'
r=requests.get(home_url,timeout=(1000000,1000000),verify=False)
print(r.text)
# with requests.session() as c:
#     # r=waitForResourceAvailable(c,'get',home_url)
#     # print('done r')
#     # with open('start' + '.html', 'wb') as f:
#     #     f.write(r.content)
#     params={
#         'citizenshipID':'269',
#         'statusType':'--SELECT--'
#     }
#     res=waitForResourceAvailable(c,'post',next_url,params=params)
#     print('done res')
#     # rest=waitForResourceAvailable(c,'get',next_url)
#     with open('hey' + '.html', 'wb') as f:
#         f.write(res.content)
# with requests.session() as c:
#     c.get('https://www.facebook.com/')
#     r=c.post('https://www.facebook.com/',data={'email':'9847282673','pass':'9847282'})
#     with open('insta.html', 'wb') as f:
#             f.write(r.content)