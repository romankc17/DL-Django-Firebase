from django.test import TestCase
from PIL import Image
import requests
from io import BytesIO,StringIO

# class CaptchaImageTest(TestCase):
#     def test_captcha_image(self):
#         response = self.client.get('/captcha/image/')

img = requests.get('https://picsum.photos/id/237/200/300')
img = Image.open(BytesIO(img.content))

basewidth = 300
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((200, 50), Image.ANTIALIAS)



output = BytesIO()
img.save(output, format='JPEG')

contents = output.getvalue().decode("base64")
output.close()
print(contents)
