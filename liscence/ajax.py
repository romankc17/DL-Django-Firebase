import time
from bs4 import BeautifulSoup
import datetime
from _firebase import send_password_reset_email
from django.http import Http404, JsonResponse
from firebaseDb import clients, users
from .models import Cookies
from .request_sess import waitforResponse,waitForResourceAvailable
from firebase_admin import auth

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


def submit_form(client,cookies,captcha,current_user):
    cookies = {'JSESSIONID':cookies}
    person_detail = {
        'dlOnlineReg.firstname': client.firstname,
        'dlOnlineReg.middlename': client.middlename,
        'dlOnlineReg.lastname': client.lastname,
        'dob': client.dob,
        'dojo.dob': '',
        'dobBs': client.dobBs,
        'age': client.age,
        'dlOnlineReg.gender.id': client.gender,
        'dlOnlineReg.occupation': '',
        'dlOnlineReg.education': '',
        'dlOnlineReg.bloodgroup.id': client.bloodgroup,
        'citizenshipID': client.citizenshipID,
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
    payload = {'citizenshipID': '269',
                'statusType': 'NEWLICENSE',
                'action:saveApplicationEntry': 'SAVE DETAILS',
                'statusType': 'NEWLICENSE'}
    start = time.perf_counter()

    # First Url
    res=waitforResponse(cookies, 'post',
                                   'https://onlineedlreg.dotm.gov.np/applicationSummaryInfo.action',
                                   params=person_detail)
    with open(client.firstname+'.html', 'wb') as f:
        f.write(res.content)
    statusInfo('first',res)

    # Second Url
    res = waitforResponse(cookies,
                        'post',
                        "https://onlineedlreg.dotm.gov.np/applicationSummaryInfo.action",
                        params=payload)
    with open(client.firstname+'final.html', 'wb') as f:
        f.write(res.content)
    statusInfo('second',res)

    finish = time.perf_counter()
    soup = BeautifulSoup(res.content, 'html.parser')
    for _ in range(3):
        try:
            ref_no = soup.find('input', attrs={'name': 'referenceNo'})
            ref_no = ref_no['value']
            payload = {'successMessage': 'APPLICATION SAVED SUCCESSFULLY REFERENCE NO: ' + ref_no,
                    'referenceNo': ref_no,
                    'applicantfullname': (soup.find('input', attrs={'name': 'applicantfullname'}))['value'],
                    'regdate': (soup.find('input', attrs={'name': 'regdate'}))['value'],
                    'status': (soup.find('input', attrs={'name': 'status'}))['value'],
                    'citizenshipnumber': (soup.find('input', attrs={'name': 'citizenshipnumber'}))['value'],
                    'expiryDate': (soup.find('input', attrs={'name': 'expiryDate'}))['value'],
                    'bloodgroup': (soup.find('input', attrs={'name': 'bloodgroup'}))['value'],
                    'dobStr': (soup.find('input', attrs={'name': 'dobStr'}))['value'],
                    'mobilenumber': (soup.find('input', attrs={'name': 'mobilenumber'}))['value'],
                    'selectedcategories': (soup.find('input', attrs={'name': 'selectedcategories'}))['value'],
                    'fathername': (soup.find('input', attrs={'name': 'fathername'}))['value'],
                    'Address': (soup.find('input', attrs={'name': 'Address'}))['value'],
                    'appointmentDate': (soup.find('input', attrs={'name': 'appointmentDate'}))['value'],
                    'applyZone': (soup.find('input', attrs={'name': 'applyZone'}))['value'],
                    'applyOffice': (soup.find('input', attrs={'name': 'applyOffice'}))['value']}

            # updating  db with submit and payload
            client.update({'payload': payload,
                           'submitted_by': current_user,
                           'submitted': True,
                           'clientSubmittedAt': datetime.now(local)})
            data = {'info': notice + f'\t({(finish - start)} seconds)',
                    'submitted': False}
            return data
        except:
            notice = (f"Not Registered!!!")
            data = {'info': notice+f'\t({(finish-start)} seconds)',
                    'submitted': False}

    return data


def captcha_entry(request):
    time.sleep(2)
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
        id = obj.id
        return JsonResponse({'img_url': img_url, 'sess':sess, 'id':id})
    else:
        raise Http404()

def submit_captcha(request):
    if request.method=="POST" and request.is_ajax():
        sess = request.POST.get('session')
        captcha_text = request.POST.get('captcha')
        client_id=request.POST.get('client_id')
        client = clients.get_by_id(client_id)
        data=submit_form(client,sess,captcha_text.strip(),request.user)
        return JsonResponse(data)
    else:
        raise Http404()

def delete_client(request):
    if request.method=='POST' and request.is_ajax():
        id = request.POST.get('id')
        clients.delete(str(id))
        return JsonResponse({'a':'a'})
    else:
        raise Http404()

def reset_password(request):
    if request.is_ajax():
        email=request.GET.get('email')
        print(email)
        sent=send_password_reset_email(email.strip())
        print(sent)
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
            clients.update(id,updates)
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
                 'clientSubmittedAt':datetime.datetime.now(local)
                 }
        data={}
        try:
            clients.update(client_id,updates)
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
            clients.update(client_id,updates)
            data['updated']=True
            data['msg']='Successfully Updated!!'
        except Exception as ec:
            data['updated']=False
            data['msg']=str(ec)
        return JsonResponse(data)
    return Http404('Invalid Request!!')


