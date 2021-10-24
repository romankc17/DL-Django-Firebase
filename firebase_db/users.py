from firebase_admin import auth
import smtplib
import json
import requests


class User:
    
    '''
        uid,
        custom_claims
        display_name,
        email,
        email_verified,
        phone_number,
        photo_url,
        tenant_id,
    '''
    
    def __init__(self):
        self.api_key = 'AIzaSyC0xnr3u6UdBSr8B92RrmuhSHHWOxoyEWU'
    
    def all(self) -> list:
        users = auth.list_users().users
        return users
    
    def get(self,**kwargs) -> auth.UserRecord:
        if len(kwargs) > 1:
            raise ValueError('Too many arguments')
        if len(kwargs) == 0:
            raise ValueError('No arguments')
        
        key = list(kwargs.keys())[0]
        
        if key=='uid':
            user = auth.get_user(kwargs['uid'])
            return user
        
        if key=='email':
            return auth.get_user_by_email(kwargs['email'])
        
        if key=='phone_number':
            return auth.get_user_by_phone_number(kwargs['phone_number'])
        
        if key=='display_name':
            return auth.get_user_by_display_name(kwargs['display_name'])
        
    def create(self, **kwargs):
        user = auth.create_user(**kwargs)
        return user
        
    def delete(self, uid):
        auth.delete_user(uid)
        
    def update(self,uid, **kwargs):
        user = auth.update_user(uid,**kwargs)
        return user
    
    def set_staff(self,uid):  
        auth.set_custom_user_claims(uid, {'staff': True,'admin':False})
     
    def get_staffs(self,users_list=None):
        if users_list is None:
            users_list = self.all()
        staffs = []
        for user in users_list:
            try:
                if user.custom_claims['staff']:
                    staffs.append(user)
            except Exception as e:
                pass
        return staffs
    
    def send_password_reset_email(self, email):
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(self.api_key)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
        request_object = requests.post(request_ref, headers=headers, data=data)
        # raise_detailed_error(request_object)
        return request_object.json()
        
              
if __name__ == '__main__':
    from initialize import initialize_firebase
    initialize_firebase()
    user  = User()
    user_data = {
        'email':'user@example.com',
        'email_verified':False,
        'phone_number':'+15555550100',
        'password':'secretPassword',
        'display_name':'John Doe',
        'photo_url':'http://www.example.com/12345678/photo.png',
        'disabled':False
    }
    print(user.send_password_reset_email('romdanchhetri02@gmail.com'))

