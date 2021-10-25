import requests
from bs4 import BeautifulSoup
import re
url='https://www.ashesh.com.np/nepali-date-converter.php'


months = {
    'January':1, 
    'February':2, 
    'March':3, 
    'April':4, 
    'May':5, 
    'June':6, 
    'July':7, 
    'August':8, 
    'September':9, 
    'October':10, 
    'November':11, 
    'December':12
}

def bs_to_ad(year,month,day):
    response = requests.post(
        url,
        data={
            'year': year,
            'month':month,
            'day':day,
            'submit':'Convert'
        }
    )
    
    soup = BeautifulSoup(response.content,'html.parser')
    a=soup.find_all("div", class_="inner")[1]
    dAD=a.text[3:]
    
    pattern = re.compile(r'(\d{4})\s([A-Za-z]+)\s(\d{1,2})')
    match = pattern.findall(dAD)[0]
    
    year = match[0]
    month = str(months[match[1]])
    day = match[2]
    
    if len(month) == 1:
        month = '0' + month
    
    if len(day)==1:
        day='0'+day
    
    
    return year,month,day  

    
if __name__ == '__main__':
    d = bs_to_ad('2022','1','25')
    print(d)