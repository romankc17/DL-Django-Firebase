import time
from bs4 import BeautifulSoup
import datetime
from django.http import Http404, JsonResponse

from .models import Cookies
from .request_sess import waitforResponse
from firebase_admin import auth
from datetime import datetime as dt

from firebase_db import clients, users
client_obj=clients.Client()
user_obj=users.User()

import pytz
local=pytz.timezone('Asia/Kathmandu')


def statusInfo(pos,res):
    print(f'###############{pos}############################')
    print('url: ' + res.url)
    print(f'status_code:{res.status_code}')
    print('raise_for_status',res.raise_for_status())
    print(f"isRedirect?: {res.is_redirect}")
    print(f'HistoryCodes:{res.history}')
    for i, response in enumerate(res.history, 1):
        print(i, response.url)


# def submit_form(client,cookies,captcha,captcha2,current_user):
#     print(captcha,captcha2)
#     cookies = {'JSESSIONID':cookies}
#     print(cookies)
#     person_detail = {
#         'dlOnlineReg.firstname': client.firstname,
#         'dlOnlineReg.middlename': client.middlename,
#         'dlOnlineReg.lastname': client.lastname,
#         'dob': client.dob,
#         'dojo.dob': '',
#         'dobBs': '',
#         'age': '30',
#         'dlOnlineReg.gender.id': client.gender,
#         'dlOnlineReg.occupation': '',
#         'dlOnlineReg.education': '',
#         'dlOnlineReg.bloodgroup.id': client.bloodgroup,
#         'citizenshipID': '269',
#         'dlOnlineReg.citizenshipnumber': client.citizenshipNumber,
#         'dlOnlineReg.districtByIssuedistrictid.id': client.citizenshipDistrict,
#         'dlOnlineReg.passportnumber': '',
#         'dlOnlineReg.countryByPassportcountryId.id': '-1',
#         'dlOnlineReg.identitymark': '',
#         'dlOnlineReg.witnessFirstname': client.witnessFirstname,
#         'dlOnlineReg.witnessMiddlename': client.witnessMiddlename,
#         'dlOnlineReg.witnessLastname': client.witnessLastname,
#         'dlOnlineReg.relationtype.id': client.relationtype,
#         'dlOnlineReg.trainerName': '',
#         'dlOnlineReg.trainerLicenseno': '',
#         'dlOnlineReg.zoneByPermZone.id': client.zone,
#         'dlOnlineReg.districtByPermDistrict.id': client.district,
#         'dlOnlineReg.villagemetrocityByPermVillagemetrocity.id': client.village,
#         'dlOnlineReg.permWardnumber': client.wardNumber,
#         'dlOnlineReg.permTole': client.tole,
#         'dlOnlineReg.permBlocknumber': '',
#         'dlOnlineReg.permMobilemumber': client.mobileNumber,
#         'dlOnlineReg.permOfficecontact': '',
#         'dlOnlineReg.permContactnumber': '',
#         'dlOnlineReg.permEmail': '',
#         'dlOnlineReg.zoneByZoneId.id': client.zone,
#         'dlOnlineReg.districtByDistrictId.id': client.district,
#         'dlOnlineReg.villagemetrocityByVillagemetrocityId.id': client.village,
#         'dlOnlineReg.wardnumber': client.wardNumber,
#         'dlOnlineReg.tole': client.tole,
#         'dlOnlineReg.blocknumber': '',
#         'dlOnlineReg.mobilenumber': client.mobileNumber,
#         'dlOnlineReg.contactoffice': '',
#         'dlOnlineReg.contactnumber': '',
#         'dlOnlineReg.email': '',
#         'chkAddress': 'true',
#         '__checkbox_chkAddress':'true',
#         'cate': client.cate,
#         'dlOnlineReg.zoneByAppliedZoneoffice.id': client.appliedZoneOffice,
#         'dlOnlineReg.licenseissueoffice.id': client.licenseIssueOffice,
#         'jcaptcha': captcha,
#         'statusType': 'NEWLICENSE',
#         'saveDetails': 'SUBMIT'
#     }
#     payload = {'citizenshipID': '269',
#                 'statusType': 'NEWLICENSE',
#                 'action:saveApplicationEntry': 'SAVE DETAILS',
#                 'statusType': 'NEWLICENSE',
#                 'jcaptcha':captcha2}
#     start = time.perf_counter()

#     # First Url
#     res=waitforResponse(cookies, 'post',
#                                    'https://onlineedlreg.dotm.gov.np/Nepal_DLReg/applicationSummaryInfo.action',
#                                    params=person_detail)
#     with open('initial.html', 'w') as f:
#         f.write(res.text)
#     print('done posting')
    
#     if 'dlNewRegHome' in res.url:
#         notice = (f"Incorrect Captcha!!!")
#         data = {'info': notice,
#                 'submitted': False}
#         return data
    
#     # Second Url
#     response = waitforResponse(cookies,
#                         'post',
#                         "https://onlineedlreg.dotm.gov.np/Nepal_DLReg/applicationSummaryInfo.action",
#                         params=payload)
#     with open('final.html', 'w') as f:
#         f.write(response.text)
#     print('done saving')
#     print(response.url)
    
#     if not 'newDlApplicationEntryResult' in response.url:
#         data = {'info': 'Not Registered','submitted':False}
#         return data
    
#     url = str(response.url)
    

#     finish = time.perf_counter()
    
#     updates = {
#         'success_url': url,
#         'submitted_by': current_user,
#         'submitted': True,
#         'clientSubmittedAt': dt.now(local)
#     }
#     client_obj.update(client.id,**updates)
    
#     data = {'info': "Registered Successfully" + f'\t({(finish - start)} seconds)',
#             'submitted': True}        

#     return data


def add_category(client,cookie,captcha,current_user):
    cookies = {'JSESSIONID':cookie}
    detail = {
        'applicationNo':'',
        'dob': client.dob,
        'dojo.dob': '',
        'dobBs': '',
        'licenseNo': client.licenseNo,
        'cate': client.cate,
        'dlOnlineReg.zoneByAppliedZoneoffice.id': client.appliedZoneOffice,
        'dlOnlineReg.licenseissueoffice.id': client.licenseIssueOffice,
        'jcaptcha': captcha.strip(),
        'statusType': 'ADDCATEGORY',
        'saveDetails': 'SUBMIT'
    }
    url = 'https://onlineedlreg.dotm.gov.np/Nepal_DLReg/saveAddcategoryEntry.action'
    response = waitforResponse(cookies,'post',url,params=detail)
    
    if 'newDlApplicationEntryResult' in str(response.url):
        client.update(**{
            'success_url': response.url,
            'submitted_by': current_user,
            'submitted': True,
            'clientSubmittedAt': dt.now(local)
        })
        notice = (f"Successfully Category Added!!!")
        data = {'info': notice,
                'submitted': True}
    else:
        notice = (f"Not Registerd")
        data = {'info': notice,'submitted':False}
    data.update({'statusType':'addcategory'})
    return data

def captcha_entry(request):
    
    if request.method=="POST" and request.is_ajax():
        obj = Cookies()
        # calling method to save captcha
        cookies=obj.get_remote()
        # getting cookie object
        obj = Cookies.objects.get(session=cookies)
        # captcha image url
        img_url = str(obj.captcha.url)
        
        #cookie
        sess = str(obj.session)
        print('this',sess)
        id = obj.id
        return JsonResponse({'img_url': img_url, 'sess':sess, 'id':id})
    else:
        raise Http404()


def submit_client(request):
    if request.method=="POST" and request.is_ajax():
        cookie = request.POST.get('session')
        captcha = request.POST.get('captcha').strip()
        client_id=request.POST.get('client_id')
        client = client_obj.get_by_id(client_id)
        
        if client.statusType == 'addcategory':
            data = add_category(client,cookie,captcha,request.user.username)
            return JsonResponse(data)
        else:
            cookies = {'JSESSIONID':cookie}
            person_detail = {
                'dlOnlineReg.firstname': client.firstname,
                'dlOnlineReg.middlename': client.middlename,
                'dlOnlineReg.lastname': client.lastname,
                'dob': client.dob,
                'dojo.dob': '',
                'dobBs': '',
                'age': '30',
                'dlOnlineReg.gender.id': client.gender,
                'dlOnlineReg.occupation': '',
                'dlOnlineReg.education': '',
                'dlOnlineReg.bloodgroup.id': client.bloodgroup,
                'citizenshipID': '269',
                'dlOnlineReg.citizenshipnumber': client.citizenshipNumber,
                'dlOnlineReg.districtByIssuedistrictid.id': client.citizenshipDistrict,
                'dlOnlineReg.passportnumber': '',
                'dlOnlineReg.countryByPassportcountryId.id': '-1',
                'dlOnlineReg.identitymark': '',
                'dlOnlineReg.witnessFirstname': client.witnessFirstname,
                'dlOnlineReg.witnessMiddlename': client.witnessMiddlename,
                'dlOnlineReg.witnessLastname': client.witnessLastname,
                'dlOnlineReg.relationtype.id': client.relationtype,
                'dlOnlineReg.trainerName': '',
                'dlOnlineReg.trainerLicenseno': '',
                'dlOnlineReg.zoneByPermZone.id': client.zone,
                'dlOnlineReg.districtByPermDistrict.id': client.district,
                'dlOnlineReg.villagemetrocityByPermVillagemetrocity.id': client.village,
                'dlOnlineReg.permWardnumber': client.wardNumber,
                'dlOnlineReg.permTole': client.tole,
                'dlOnlineReg.permBlocknumber': '',
                'dlOnlineReg.permMobilemumber': client.mobileNumber,
                'dlOnlineReg.permOfficecontact': '',
                'dlOnlineReg.permContactnumber': '',
                'dlOnlineReg.permEmail': '',
                'dlOnlineReg.zoneByZoneId.id': client.zone,
                'dlOnlineReg.districtByDistrictId.id': client.district,
                'dlOnlineReg.villagemetrocityByVillagemetrocityId.id': client.village,
                'dlOnlineReg.wardnumber': client.wardNumber,
                'dlOnlineReg.tole': client.tole,
                'dlOnlineReg.blocknumber': '',
                'dlOnlineReg.mobilenumber': client.mobileNumber,
                'dlOnlineReg.contactoffice': '',
                'dlOnlineReg.contactnumber': '',
                'dlOnlineReg.email': '',
                'chkAddress': 'true',
                '__checkbox_chkAddress':'true',
                'cate': client.cate,
                'dlOnlineReg.zoneByAppliedZoneoffice.id': client.appliedZoneOffice,
                'dlOnlineReg.licenseissueoffice.id': client.licenseIssueOffice,
                'jcaptcha': captcha,
                'statusType': 'NEWLICENSE',
                'saveDetails': 'SUBMIT'
            }
            res=waitforResponse(
                cookies, 
                'post',
                'https://onlineedlreg.dotm.gov.np/Nepal_DLReg/applicationSummaryInfo.action',
                params=person_detail
            )
            with open('initial.html', 'w') as f:
                f.write(res.text)
            print('done posting')
            obj = Cookies.objects.get(session=cookie)
            obj = obj.save_second_captcha()
            img_url = str(obj.captcha2.url)
            return JsonResponse({'img_url': img_url})
    else:
        raise Http404()
    
    
def save_client(request):
    cookie = request.POST.get('session')
    captcha = request.POST.get('captcha').strip()
    client_id=request.POST.get('client_id')
    client = client_obj.get_by_id(client_id)
    
    print(client_id,captcha,cookie)
    
    cookies = {'JSESSIONID':cookie}
    payload = {
        'citizenshipID': '269',
        'statusType': 'NEWLICENSE',
        'action:saveApplicationEntry': 'SAVE DETAILS',
        'statusType': 'NEWLICENSE',
        'jcaptcha':captcha,
    }
    response = waitforResponse(
        cookies,
        'post',
        "https://onlineedlreg.dotm.gov.np/Nepal_DLReg/applicationSummaryInfo.action",
        params=payload
    )
    with open('final.html', 'w') as f:
        f.write(response.text)
    print('done saving')
    print(response.url)
    
    if not 'newDlApplicationEntryResult' in response.url:
        data = {'info': 'Not Registered','submitted':False}
        return JsonResponse(data)
    
    url = str(response.url)    
    
    updates = {
        'success_url': url,
        'submitted_by': request.user.username,
        'submitted': True,
        'clientSubmittedAt': dt.now(local)
    }
    client_obj.update(client.id,**updates)
    
    data = {'info': "Registered Successfully",
            'submitted': True}        

    return JsonResponse(data)
    

def delete_client(request):
    if request.method=='POST' and request.is_ajax():
        id = request.POST.get('id')
        client_obj.delete(str(id))
        return JsonResponse({'a':'a'})
    else:
        raise Http404()

def reset_password(request):
    if request.is_ajax():
        email=request.GET.get('email')
        reset = user_obj.send_password_reset_email(email)
        if 'error' not in reset.keys():
            sent=1
        else:
            sent=0
        return JsonResponse({'sent':sent})

def user_update(request):
    if request.is_ajax():
        email=request.POST.get('email')
        uid=request.POST.get('uid')
        phNumber=request.POST.get('phNumber')
        displayName=request.POST.get('displayName')
        staff=request.POST.get('staff')

        if not phNumber:
            phNumber=None

        data={}

        try:
            user=auth.update_user(
                uid,
                email=email,
                phone_number=phNumber,
                display_name=displayName
            )
            if staff=='true':
                auth.set_custom_user_claims(uid,{'staff':True,'admin':users.get_by_id(uid).admin})
            else:
                auth.set_custom_user_claims(uid, {'staff': False,'admin':users.get_by_id(uid).admin})
            print('updated')
            data['updated']=True
            data['error']=False
        except Exception as ec:
            data['updated']=False
            data['error']=str(ec)
            print(str(ec))

        return JsonResponse(data)

def client_update(request):
    if request.is_ajax():
        id=request.POST.get('id')
        allow=request.POST.get('allow')
        entry_users=request.POST.get('entry_users').strip().replace("\"","")
        updates={}
        if allow=='true':
            updates['allow']=True
        else:
            updates['allow']=False
        updates['entry_users']=list(entry_users.replace("'","").split(","))
        print(updates)
        data={}
        try:
            client_obj.update(id,**updates)
            data['updated']=True
        except Exception as ec:
            data['updated'] = False
            data['error'] = str(ec)
            print(str(ec))
        return JsonResponse(data)

def user_delete(request):
    if request.is_ajax():
        uid=request.POST.get('uid')
        data={}
        try:
            auth.delete_user(uid)
            data['deleted']=True
        except :
            data['deleted']=False

    return JsonResponse(data)

def subUpdate(request):
    if request.is_ajax() and request.method=='POST':
        client_id=request.POST.get('client_id')
        refNo=request.POST.get('refNo')

        updates={'refNo':refNo,
                 'submitted':True,
                 'clientSubmittedAt':dt.now(local)
                 }
        data={}
        try:
            client_obj.update(client_id,**updates)
            data['updated']=True
            data['message']="Successfully Updated"
        except Exception as ec:
            data['updated']=False
            data['message']=str(ec)
        return JsonResponse(data)
    return Http404('Invalid Request!!')

def mobileUpdate(request):
    if request.is_ajax() and request.method=='POST':
        client_id=request.POST.get('client_id')
        mobileNumber=request.POST.get('mobileNumber')

        updates={'mobileNumber':mobileNumber}
        data={}
        try:
            client_obj.update(client_id,**updates)
            data['updated']=True
            data['message']="Successfully Updated"
        except Exception as ec:
            data['updated']=False
            data['message']=str(ec)
        return JsonResponse(data)
    return Http404('Invalid Request!!')

def allowUpdate(request):
    if request.is_ajax() and request.method=='POST':
        client_id=request.POST.get('client_id')
        allow=request.POST.get('allow')
        print(client_id,allow)
        if allow=='true':
            allow=True
        else:
            allow=False
        data={}
        try:
            data['allow']=allow
            client_obj.update(client_id, **{'allow':allow})
            data['updated']=True
            data['message']="Successfully Updated"
        except Exception as ec:
            data['updated']=False
            data['message']=str(ec)
        return JsonResponse(data)
    return Http404('Invalid Request!!')

def edit_entryUsers(request):
    if request.is_ajax and request.method=='POST':
        client_id=request.POST.get('client_id')
        entryUsers=request.POST.get('entryUsers')

        updates={
            'entry_users':entryUsers.split(',')
        }
        data={}
        try:
            client_obj.update(client_id,**updates)
            data['updated']=True
            data['msg']='Successfully Updated!!'
        except Exception as ec:
            data['updated']=False
            data['msg']=str(ec)
        return JsonResponse(data)
    return Http404('Invalid Request!!')



def get_clients(request):
    LIMIT = 40
    if request.is_ajax():
        staff = request.POST.get('staff')
        if staff == "":
            staff = None
        last_client_added_date = request.POST.get('last_client_added_at')
        
        data={}
        if last_client_added_date == 'None':
            last_client_added_date = None
        else:
            try:
                last_client_added_date = datetime.datetime.strptime(last_client_added_date,'%Y-%m-%d %H:%M:%S.%f',)
            except:
                last_client_added_date = datetime.datetime.strptime(last_client_added_date,'%Y-%m-%d %H:%M:%S')
            
        clients, last_client_added_date = client_obj.getNClients(
                limit=LIMIT,
                last_doc_clientAddedAt=last_client_added_date,
                staff = staff
            )
        if len(clients) < LIMIT:
            data['nomore'] = True
        else:
            data['nomore'] = False
        data['clients']=[client.__dict__ for client in clients]
        data['last_client_added_at']=str(last_client_added_date)[:-6]
        
        return JsonResponse(data)
    else:
        return Http404('Invalid Request!!')

def search_clients(request):
    if request.is_ajax():
        if not request.user.is_superuser:
            staff = request.user.username
        else:
            staff = None    
        value = request.GET.get('value')
        clients = client_obj.search(value,staff=staff)
        return JsonResponse({'clients':[client.__dict__ for client in clients]})