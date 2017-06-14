from PIL import Image
import mechanize,cookielib
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import json
from Captcha_Parser import CaptchaParse
import ssl
import os
import sys
import datetime
import time
def calsem():
        now = datetime.datetime.now()
        if int(now.month)>6 and int(now.month)<13:
                sem="FS"
        else:
                sem="WS"
        return sem
br= mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
def internet():
    try:
        br.open('http://216.58.192.142')
        return True
    except mechanize.URLError as err:
        return False
if internet() is False:
        print "Please connect to the internet and restart the application.The application will close."
        os.remove("clientsecret.json")
        os.remove("storage.json")
        time.sleep(3)
        sys.exit()
def OpenLink():
        try:
                _create_unverified_https_context=ssl._create_unverified_context
        except AttributeError:
                pass
        else:
                ssl._create_default_https_context=_create_unverified_https_context
        r=br.open('https://vtop.vit.ac.in/parent/parent_login.asp')
        html=r.read()
        soup=BeautifulSoup(html)
        im = soup.find('img', id='imgCaptcha')
        image_response = br.open_novisit(im['src'])
        img=Image.open(StringIO(image_response.read()))
        return img
def GetDetails():        
        name=raw_input("Name:")
        regno=raw_input("Registration Number:")
        dob=raw_input("Date of Birth(DDMMYYYY):")
        mno=raw_input("Registered Parent Mobile Number:")
        pmno=raw_input("Personal Mobile Number:")
        email=raw_input("Email ID:")
        skills=raw_input("Enter skills seperated by '/':")
        DetailFile=open("Details of "+regno+".txt","w")
        DetailFile.write(name+'\n'+regno+'\n'+pmno+'\n'+email+'\n'+skills)
        DetailFile.close()
        return [regno,dob,mno]
detail=GetDetails()
print "Logging in User:"
captchacount=0
while True:
        count=0
        img=OpenLink()
        br.select_form('parent_login')
        br.form['wdregno']=detail[0]
        br.form['wdpswd'] =detail[1]
        br.form['wdmobno']=detail[2]
        captcha=CaptchaParse(img)
        br.form['vrfcd']=captcha
        response=br.submit()
        if(response.geturl()=="https://vtop.vit.ac.in/parent/home.asp"):
                print "Successfully Logged In"
                break
        else:
                captchacount+=1
                print "Retrying Captcha "
        if captchacount==5:
                print "You seem to have entered incorrect Credentials.Please enter the right credentials.\n\n"
                detail=GetDetails()
        
mainpage=br.open(response.geturl()).read()
mainsoup=BeautifulSoup(mainpage)
sem=calsem()
ttasp=br.open('https://vtop.vit.ac.in/parent/timetable.asp?sem='+sem)
tthtml=ttasp.read()
ttsoup=BeautifulSoup(tthtml)
slotlist=[]
row1=[]
row2=[]
table=ttsoup.find('table',attrs={'cellpadding':'2','border':'1','cellspacing':'0','width':'95%','style':'border-collapse: collapse'})
for mainrow in table.findAll("tr"):
        cells=mainrow.findAll('td',attrs={'bgcolor':'#FFFFCC'})
        for i in cells:
                slotlist.append(str(i.find('font',attrs={"color":"#99CCFF"})))
        newcells=mainrow.findAll('td',attrs={'bgcolor':'#CCFF33'})
        for i in newcells:
                row1.append(i.find(text=True).encode("utf-8"))
for i in row1:
        if i not in row2:
                row2.append(i)
venueslot=[]
venue=[]
slot=[]
count=0
for i in row2:
        for j in range(0,len(i)-1):
                if i[j]=='-':
                       count+=1
                if count==2:
                       newstr=i[j+2:len(i)]
                       venueslot.append(newstr)
                       count=0
                       break
for i in venueslot:
        for j in range(0,len(i)-1):
                if i[j]=='-':
                        venuestr=i[0:j-1]
                        slotstr=i[j+2:len(i)]
                        if venuestr[len(venuestr)-1].isalpha():
                                venuestr=venuestr[:-4]
                        else:
                                venuestr=venuestr[:-3]
                        if venuestr[len(venuestr)-1]=='G':
                                venuestr=venuestr[:-1]
                        venue.append(venuestr)
                        slot.append(slotstr)
regno=detail[0]
fileout=open("Slots of "+regno+".txt","w")
for i in slot:
        fileout.write(i+'\n')
fileout.close()
fileout=open("Venues of "+regno+".txt","w")
for i in venue:
        fileout.write(i+'\n')
fileout.close()

fout=open("Free slots of "+regno+".txt","w")
for i in slotlist:
        if i!='None':
                str1=i[22:len(i)]
                str2=str1[:-7]
                if len(str2)==5 or len(str2)==6:
                        str2=str2[4:len(str2)]
                        if int(str2)<61:
                                fout.write(str2+'\n')
fout.close()
