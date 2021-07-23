import datetime
import pytz
local=pytz.timezone('Asia/Kathmandu')

from firebaseDb import clients,institutes,users
from firebase_admin import auth,firestore
db = firestore.client()


from django.http import Http404
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Cookies, Client
from .request_sess import *

def is_staff(user):
    return  user.is_staff

def is_superuser(user):
    return  user.is_superuser

def sortClients(_clients,reverse=False):
    _clients = sorted(_clients, key=lambda x: x.clientAddedAt, reverse=reverse)
    return _clients


@login_required
def index(request):
    # deleting cookies if exist before creating session
    for cookie in Cookies.objects.all():
        cookie.captcha.delete(save=True)
        cookie.delete()
    # to_be_enterd = request.user.client_set.filter(submitted=False)
    from firebaseDb import clients
    if request.user.is_superuser:
        _clients=clients.filter(submitted=False,allow=True)
    else:
        _clients = clients.for_staff_sub(request.user)
    _clients = sorted(_clients, key=lambda x: x.clientAddedAt, reverse=False)
    counts = len(_clients)
    # clients=sorted(to_be_entered, key=lambda x: random.random())
    context={'user':request.user,
             'counts':counts,
             'clients': _clients}
    return render(request, 'liscence/index.html',context )
        

@user_passes_test(is_staff)
def list_clients(request):
    payload={}
    if request.user.is_superuser:
        _clients=sortClients(clients.all(),reverse=True)
        _users = users.all()
        payload.update({'institutes':institutes.all(),
                        'users':users.all(),
                        'staffs':[user for user in _users if user.staff],
                        'submitted_by':'all',
                        'entry_users':'all',
                        'allow_clients':'all',
                        'staff': 'all'
                        })
    else:
        _clients = sortClients(clients.filter(staff=request.user.username),reverse=True)
    payload.update({'submitted_all': True, 'cate_all': True, 'added_at_all': True, 'submitted_at_all': True,})
    payload.update({'clients':_clients,'counts':len(_clients)})
    return render(request,'liscence/client_list.html',payload)


def clients_filter(request):
    submitted = request.POST['submitted']
    category = request.POST['cate']
    clientAddedAt = request.POST['added_date']
    clientSubmittedAt = request.POST['submitted_date']

    to_filter = {}
    payload = {}

    if request.method == 'POST':
        if request.user.is_superuser:
            staff = request.POST['staffs']
            submitted_by=request.POST['submitted_by']
            entry_users=request.POST['entry_users']
            allow_clients=request.POST['allow_clients']
            payload['staff']=staff
            payload['submitted_by']=submitted_by
            payload['entry_users']=entry_users
            payload['staffs']=users.filter_by_staff()
            if not staff=='all':
                to_filter['staff']=staff
            print(allow_clients)
            if not allow_clients=='all':
                if allow_clients=='yes':
                    allow=True
                else:
                    allow=False
                to_filter['allow']=allow
            payload['allow_clients']=allow_clients
            if not submitted_by=='all':
                to_filter['submitted_by']=submitted_by
            if not entry_users=='all':
                to_filter['entry_users']=entry_users
            _users = users.all()
            payload['users']=_users

            if staff==submitted_by==submitted == category == clientAddedAt == clientSubmittedAt==entry_users==allow_clients=='all':
                return redirect('clients')
        else:
            if submitted==category==clientAddedAt==clientSubmittedAt=='all':
                return redirect('clients')

        cate_dict = {'A': '1', 'K': '50', 'B': '2', 'C': '3', 'C1': '23'}
        if not category=='all':
            cate = cate_dict[category]
            to_filter['cate']=cate
            payload['cate'+category]=True
        else:
            payload['cate_all']=True

        if not submitted=='all':
            if submitted == 'yes':
                to_filter['submitted']=True
                payload['submitted_yes']=True
            else:
                to_filter['submitted']=False
                payload['submitted_no'] = True
        else:
            payload['submitted_all']=True

        today = datetime.date.today()
        week_ago = datetime.datetime.combine((today - datetime.timedelta(days=7)),datetime.datetime.min.time())
        month_ago = datetime.datetime.combine((today - datetime.timedelta(days=30)),datetime.datetime.min.time())
        today=datetime.datetime.combine(today,datetime.datetime.min.time())

        if not clientAddedAt=='all':
            if clientAddedAt=='today':
                to_filter['clientAddedAt']=today
            elif clientAddedAt == 'week':
                to_filter['clientAddedAt']=week_ago
            else:
                to_filter['clientAddedAt'] = month_ago
        payload['added_at_' + clientAddedAt] = True

        if not clientSubmittedAt=='all':
            if clientSubmittedAt=='today':
                to_filter['clientSubmittedAt']=today
            elif clientSubmittedAt == 'week':
                to_filter['clientSubmittedAt']=week_ago
            else:
                to_filter['clientSubmittedAt'] = month_ago
        payload['submitted_at_'+clientSubmittedAt]=True
        if not request.user.is_superuser:
            to_filter['staff']=request.user.username
        print(to_filter)
        _clients=clients.page_filter(to_filter)

        payload['clients']=sortClients(_clients,reverse=True)
        payload['counts']=len(_clients)
        return render(request,'liscence/client_list.html',payload)
    else:
        raise Http404()


@user_passes_test(is_staff)
def success_link(request, client_id):
    client=clients.get_by_id(client_id)
    if hasattr(client,'success_url') and client.submitted:
        return redirect(client.success_url)
    elif hasattr(client,'refNo') and client.submitted:
        ref=client.refNo
        if client.statusType.lower() == 'addcategory':
            status = 'ADDCATEGORY'
        else:
            status = 'Registered'
        rvd=RegVisit()
        payload = {
            'successMessage': f'APPLICATION SAVED SUCCESSFULLY REFERENCE NO: {ref}',
            'referenceNo': ref,
            'applicantfullname': client.firstname + " " + client.middlename + " " + client.lastname,
            'regdate': rvd.getRegDate(),
            'status': status,
            'citizenshipnumber': client.citizenshipNumber,
            'expiryDate': 'N/A',
            'bloodgroup': client.displayBG,
            'dobStr': client.dob[:10],
            'mobilenumber': client.mobileNumber,
            'selectedcategories': client.category,
            'fathername': client.witnessFirstname + " " + client.witnessMiddlename + " " + client.witnessLastname,
            'Address': client.tole + " " + client.wardNumber + " " + client.districtName + " " + client.zoneName + " Nepal",
            'appointmentDate': rvd.getVisitDate(),
            'applyZone': 'Lumbini',
            'applyOffice': 'Lumbini'
        }
        url = requests.get(
            'http://onlineedlreg.dotm.gov.np/newDlApplicationEntryResult_.action',
            params=payload,
            verify=False,
            timeout=(1000, 1000),
        ).url
        return redirect(url)
    return Http404("Can't Find Url")

@user_passes_test(is_staff)
def success_link2(request, mobile,ref):
    client=clients.filter(mobileNumber=mobile)[0]
    if not client:
        return Http404('No client with this mobilenumber')
    try :
        return redirect(client.success_url)
    except:
        pass

    if client.statusType.lower() == 'addcategory':
        status='ADDCATEGORY'
    else:
        status='Registered'
    try:
        district=client.districtName
        zone=client.zoneName
    except:
        district=client.district
        zone=client.zone
    payload = {'successMessage': f'APPLICATION SAVED SUCCESSFULLY REFERENCE NO: {ref}',
               'referenceNo': ref,
               'applicantfullname': client.firstname+" "+client.middlename+" "+client.lastname,
               'regdate': '1/7/21',
               'status': status,
               'citizenshipnumber': client.citizenshipNumber,
               'expiryDate': 'N/A',
               'bloodgroup': client.displayBG,
               'dobStr': client.dob[:10],
               'mobilenumber': client.mobileNumber,
               'selectedcategories': client.category,
               'fathername': client.witnessFirstname+" "+client.witnessMiddlename+" "+client.witnessLastname,
               'Address': client.tole+" "+client.wardNumber+" "+district+" "+zone+" Nepal",
               'appointmentDate': '1/13/21',
               'applyZone': 'Lumbini',
               'applyOffice': 'Lumbini'}
    r = requests.get('http://onlineedlreg.dotm.gov.np/newDlApplicationEntryResult_.action',
                     params=payload,
                     verify=False,
                     timeout=(1000,1000),)
    return render(request, 'liscence/success_link.html', {"link":r.url})

@user_passes_test(is_superuser)
def create_user(request):
    if request.method == 'POST':
        uid=request.POST.get('username')
        display_name = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneNumber = request.POST.get('phoneNumber')
        staffCheck = request.POST.get('checkStaff')

        staff = False
        if staffCheck:
            staff=True

        try:
            ph=int(phoneNumber)
            if len(phoneNumber)!=10 and len(phoneNumber)!=0:
                messages.error(request,'Invalid PhoneNumber')
                return redirect('create_user')
        except :
            messages.error(request, 'Invalid PhoneNumber')
            return redirect('create_user')

        if phoneNumber:
            phoneNumber = '+977'+phoneNumber
        else:
            phoneNumber = None

        try:
            user = auth.create_user(
                uid=uid,
                email=email,
                email_verified=True,
                password=password,
                display_name=display_name,
                phone_number=phoneNumber,
                disabled=False)
            auth.set_custom_user_claims(user.uid, {'staff': staff,'admin':False})
            messages.success(request, 'Sucessfully created new user: {0}'.format(user.uid))
            return redirect('list_users')
        except Exception as ec:
            messages.error(request, ec)
        return redirect('create_user')
    else:
        return render(request,'liscence/create_user.html')

@user_passes_test(is_superuser)
def list_users(request):
    params={
        'us':users.all()
    }
    return render(request,'liscence/list_users.html',params)


def add_clients(request):
    if request.method=='POST':
        data={
            'firstname':request.POST.get('firstname').upper().strip(),
            'middlename':request.POST.get('middlename').upper().strip(),
            'lastname':request.POST.get('lastname').upper().strip(),
            'gender':request.POST.get('gender'),
            'bloodgroup':request.POST.get('bloodgroup'),
            'dob':str(request.POST.get('dobAd'))+'T00:00:00+05:45',
            'dobBs':request.POST.get('dobBs'),
            'age':request.POST.get('age'),
            'citizenshipNumber':request.POST.get('citizenshipNumber'),
            'citizenshipDistrict':request.POST.get('citizenshipDistrict'),
            'relationtype':request.POST.get('relationtype'),
            'witnessFirstname':request.POST.get('witnessFirstname').upper().strip(),
            'witnessMiddlename':request.POST.get('witnessMiddlename').upper().strip(),
            'witnessLastname':request.POST.get('witnessLastname').upper().strip(),
            'zone':request.POST.get('zone'),
            'district':request.POST.get('district'),
            'village':request.POST.get('village'),
            'wardNumber':request.POST.get('wardNumber'),
            'tole':request.POST.get('tole').title(),
            'mobileNumber':request.POST.get('mobileNumber'),
            'cate':request.POST.get('cate'),
            'appliedZoneOffice':request.POST.get('appliedZoneOffice'),
            'licenseIssueOffice':request.POST.get('licenseIssueOffice'),
            'citizenshipID':'269',
        }
        try:
            staff=request.POST.get('staff').strip()
        except :
            staff=request.user
        data.update({
            'allow':True,
            'staff':staff,
            'clientAddedAt':datetime.datetime.now(local),
            'entry_users':[staff,'romanchhetri02'],
            'institute_id':'L2NNi7gACKofVU456A2t',
            'statusType':'newlicense',
            'zoneName':request.POST.get('zoneName').strip().title(),
            'districtName':request.POST.get('districtName').strip().title(),
            'submitted':False,
        })
        doc_id=data['firstname']+data['lastname']+'-'+data['mobileNumber']
        clients.add(doc_id.replace(" ",""),data)

    return render(request, 'liscence/add_clients.html')

class RegVisit:
    def __init__(self):
        regDate=datetime.datetime.now(local)-datetime.timedelta(days=1)
        self.regDate=regDate.strftime("%m/%d/%y")
        self.visitDate=(regDate+datetime.timedelta(days=6)).strftime("%m/%d/%y")

    def setDate(self,regDate,visitDate):
        self.regDate=regDate
        self.visitDate=visitDate

    def getRegDate(self):
        return self.regDate
    def getVisitDate(self):
        return self.visitDate
