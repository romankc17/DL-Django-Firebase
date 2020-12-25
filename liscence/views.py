import ast
import json
import random
import datetime

from firebaseDb import clients,institutes
from firebase_admin import auth,firestore
db = firestore.client()


from django.http import Http404
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Cookies, Client
from .request_sess import *

def is_staff(user):
    return  user.is_staff

def is_superuser(user):
    return  user.is_superuser


@login_required
def index(request):
    # deleting cookies if exist before creating session
    for cookie in Cookies.objects.all():
        cookie.captcha.delete(save=True)
        cookie.delete()
    # to_be_entered = request.user.client_set.filter(submitted=False)
    from firebaseDb import clients
    to_be_entered = clients.for_staff_sub(request.user)
    counts = len(to_be_entered)
    clients=sorted(to_be_entered, key=lambda x: random.random())
    context={'user':request.user,
             'counts':counts,
             'clients': clients}
    return render(request, 'liscence/index.html',context )
        

@user_passes_test(is_staff)
def list_clients(request):
    payload={}
    if request.user.is_superuser:
        _clients=clients.all()
        users = [user for user in auth.list_users().iterate_all()]
        payload.update({'institutes':institutes.all(),
                        'users':users,
                        'submitted_by':'all',
                        'inst': 'all'
                        })
    else:
        _clients = clients.filter(staff=request.user.username)
    payload.update({'submitted_all': True, 'cate_all': True, 'added_at_all': True, 'submitted_at_all': True,})
    payload.update({'clients':_clients})
    return render(request,'liscence/client_list.html',payload)


@user_passes_test(is_staff)
def success_link(request, pk):
    try:
        object = Client.objects.using('auth_db').get(id = pk)
    except:
        raise Http404
    r = requests.get('http://onlineedlreg.dotm.gov.np/newDlApplicationEntryResult_.action', params=ast.literal_eval(object.payload), verify=False)

    if request.user == object.staff:
        return render(request, 'liscence/success_link.html', {"link":r.url})
    else:
        raise Http404

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
    users=[user for user in auth.list_users().iterate_all()]
    params={
        'users':users
    }
    return render(request,'liscence/list_users.html',params)

def clients_filter(request):

    submitted = request.POST['submitted']
    category = request.POST['cate']
    clientAddedAt = request.POST['added_date']
    clientSubmittedAt = request.POST['submitted_date']


    to_filter = {}
    payload = {}

    if request.method == 'POST':
        if request.user.is_superuser:
            inst = request.POST['institutes']
            submitted_by=request.POST['submitted_by']
            payload['inst']=inst
            payload['submitted_by']=submitted_by
            payload['institutes']=institutes.all()
            if not inst=='all':
                to_filter['institute_id']=inst
            if not submitted_by=='all':
                to_filter['submitted_by']=submitted_by
            users = [user for user in auth.list_users().iterate_all()]
            payload['users']=users

            if inst==submitted_by==submitted == category == clientAddedAt == clientSubmittedAt== 'all':
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

        _clients=clients.page_filter(to_filter)

        payload['clients']=_clients

        return render(request,'liscence/client_list.html',payload)
    else:
        raise Http404()