from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

import json
import requests
from firebase_admin import auth

API_KEY = 'AIzaSyC0xnr3u6UdBSr8B92RrmuhSHHWOxoyEWU'

rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        payload = json.dumps({
            'email': username,
            'password': password,
            'returnSecureToken': True
        })

        r = requests.post(rest_api_url,
                          params={'key':API_KEY},
                          data=payload)
        try:
            localId = r.json()['localId']
            try:
                user = User.objects.get(username=localId)
                return user
            except:
                user = User(username=localId)
                claims = auth.verify_id_token(r.json()['idToken'])
                try:
                    if claims['staff'] is True:
                        user.is_staff = True
                    if claims['admin'] is True:
                        user.is_superuser = True
                except :
                    pass
                user.save()
                return user
        except Exception as ec:
            messages.error(request,r.json()['error']['message'])
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None