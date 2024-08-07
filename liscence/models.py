import time
from tempfile import NamedTemporaryFile

import requests
from django.core.files import File
from django.db import models
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth.models import User
from django.urls import reverse
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .request_sess import *



class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null = True,blank=True, related_name='staffs')
    submitted = models.BooleanField(default=False)
    payload = models.TextField(max_length=1000, blank=True,null=True)
    firstname= models.CharField(max_length=50)
    middlename= models.CharField(max_length=50, blank=True)
    lastname= models.CharField(max_length=50)
    dob=models.CharField(max_length=50)
    dobBs=models.CharField(max_length=50)
    age=models.CharField(max_length=50,)
    gender=models.CharField(max_length=50)
    bloodgroup=models.CharField(max_length=10)
    citizenshipID=models.CharField(max_length=10)
    citizenshipNumber=models.CharField(max_length=30)
    citizenshipDistrict=models.CharField(max_length=10)
    witnessFirstname=models.CharField(max_length=50)
    witnessMiddlename=models.CharField(max_length=50, blank=True)
    witnessLastname=models.CharField(max_length=50)
    relationtype=models.CharField(max_length=10)
    permZone=models.CharField(max_length=20)
    permDistrict=models.CharField(max_length=20)
    permVillage=models.CharField(max_length=20)
    permWardnumber=models.CharField(max_length=20)
    permTole=models.CharField(max_length=20)
    permMobilemumber=models.CharField(max_length=10)
    presZone=models.CharField(max_length=20)
    presDistrict=models.CharField(max_length=20)
    presVillage=models.CharField(max_length=20)
    presWardnumber=models.CharField(max_length=20)
    presTole=models.CharField(max_length=20)
    presMobilenumber= models.CharField(max_length=10)
    cate= models.CharField(max_length=10)
    zoneByAppliedZoneoffice=models.CharField(max_length=20)
    licenseissueoffice=models.CharField(max_length=20)
    captcha_text=models.CharField(max_length=10, null=True, blank=True)
    session_text=models.CharField(max_length=100, null=True, blank=True)
    client_added_at = models.DateTimeField(auto_now_add=True)
    client_submitted_at = models.DateField(blank=True,null=True)

    def __str__(self):
        return f'{self.firstname} {self.middlename} {self.lastname}'


    def is_submitted(self):
        return self.submitted
    is_submitted.boolean = True
    is_submitted.short_description = "Submitted?"
    is_submitted.admin_order_field = 'client_added_at'

    @property
    def full_name(self):
        return f"{self.firstname} {self.middlename} {self.lastname}"

    def get_absolute_url(self):
        return reverse('client_detail', kwargs={'pk': self.pk})

from PIL import Image
import random
class Cookies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    captcha = models.ImageField(blank=True, upload_to='images')
    captcha2 = models.ImageField(blank=True, upload_to='images',null=True)
    session = models.CharField(max_length=100)
    

    def get_remote(self):
        url='https://onlineedlreg.dotm.gov.np/Nepal_DLReg/jcaptcha.jpg'
        
        # url = f'https://picsum.photos/200/50'
        
        with requests.session() as sess:
            response = requestCaptcha(sess, url)
            cookie=sess.cookies.get_dict()['JSESSIONID']
            # cookie=random.randint(1,10000)
            Cookies.objects.create(session=cookie)
            
        
        file_name='jcaptcha'+str(cookie)+'.jpg'
        lf = NamedTemporaryFile()
        # Read the streamed image in sections
        for block in response.iter_content(1024 * 8):
            # If no more file then stop
            if not block:
                break
            # Write image block to temporary file
            lf.write(block)
        
        while True:
            try:
                object = Cookies.objects.get(session=cookie)
                object.captcha.save(file_name, File(lf))
                # print(self.captcha.url)
                break
            except Exception as e:
                print(e)
                pass
        return cookie   
    
    def save_second_captcha(self):
        cookie = self.session
        cookies = {'JSESSIONID':cookie}
        # url = f'https://picsum.photos/200/50'
        url = 'https://onlineedlreg.dotm.gov.np/Nepal_DLReg/jcaptcha.jpg?'
        response = waitforResponse(cookies, 'get', url,)
        file_name = 'jcaptcha2'+str(cookie)+'.jpg'
        lf = NamedTemporaryFile()
        for block in response.iter_content(1024 * 8):
            # If no more file then stop
            if not block:
                break
            # Write image block to temporary file
            lf.write(block)
            
        obj = Cookies.objects.get(session=cookie)
        obj.captcha2.save(file_name, File(lf))
        return obj
        
        
        
        
        
    
    



