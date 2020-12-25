from email.mime.multipart import MIMEMultipart
import pyrebase
import firebase_admin
from firebase_admin import credentials,auth,firestore
from firebaseConfig import firebaseConfig
# Use a service account
cred = credentials.Certificate('ServiceAccountKey.json')

rest_api_url="https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

import pyrebase

p_firebase = pyrebase.initialize_app(firebaseConfig)
pyrebase_auth = p_firebase.auth()

def _initialize():
    return firebase_admin.initialize_app(cred)

def get_api_key():
    FIREBASE_WEB_API_KEY = 'AIzaSyC0xnr3u6UdBSr8B92RrmuhSHHWOxoyEWU'
    return FIREBASE_WEB_API_KEY




def send_password_reset_email(email):
    try:
        pyrebase_auth.send_password_reset_email(email)
        return 1
    except :
        return 0

if __name__=='__main__':
    
    send_password_reset_email('romanchheetri02@gmail.com')