from decimal import Context
import random
import calendar
import django.utils.timezone as timezone
from calendar import HTMLCalendar
from django.views import View
from django.shortcuts import render, redirect
from .models import CustomUser, UserOTP, User, record
from django.contrib import messages
import mysql.connector as mcdb
from operator import itemgetter
from django.core.mail import message, send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import cv2
from pyzbar.pyzbar import decode
import time
import datetime
from django.contrib.auth.decorators import login_required


def scan(req):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)
    # used_codes = [1 , 2 , 3 , 4 , 5]
    # print(used_codes)

    camera = True
    success, frame = cap.read()
    while camera == True:
        success, frame = cap.read()

        for code in decode(frame):
            # if code.data.decode('utf-8 ') not in used_codes:
            # print('Sorry, register!')
            # print(code.data.decode('utf-8'))
            # time.sleep(5)
            # camera=False
            # elif code.data.decode('utf-8') in used_codes:
            print('Approved .You can enter!')
            x = code.data.decode('utf-8')
            print(x)
            y = datetime.datetime.now()
            current_time = y.strftime("%H:%M:%S")
            d1 = y.strftime("%Y-%m-%d")
            print(d1)
            print(current_time)
            # used_codes.append(code.data.decode('utf-8'))
            # time.sleep(1)
            camera = False
        # else:
        # pass
        
        cv2.imshow('Tesing-code-scan', frame)
        cv2.waitKey(1)
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    sqlcommand7=f'''select roll_no from STUDENT where id="{x}"'''
    cur.execute(sqlcommand7)
    value=cur.fetchall()
    res10 = list(map(itemgetter(0), value))
    print(res10[0])
    cur.close()
    waremail=req.session['email']
    obj1 = CustomUser.objects.get(id=x)
    obj2 = User.objects.get(warden_email=waremail)
    if(obj1.warden_id_id!=obj2.warden_id):
        messages.warning(req,"You cannot take entry of this student,will be taken by other warden!!")  
        return render(req, 'index_div.html') 
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    sqlcommand4 = f'''select roll_no from RECORD_TABLE where date_of_entry="{d1}" and roll_no="{res10[0]}"'''
    cur.execute(sqlcommand4)
    pp = []
    for h in cur:
        pp.append(h)
    cur.close()
    print(pp)
    if len(pp) != 0:
        messages.warning(req, 'Already registered!!!!')
        return render(req, 'index_div.html')
    # conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    # cur = conn.cursor()
    # waremail=req.session['email'] 
    # sqlcommand11=f'''select warden_id from warden where warden_email="{waremail}"'''
    # cur.execute(sqlcommand11)
    # val=cur.fetchall()
    # res9 = list(map(itemgetter(0), val))
    # print(res9[0])
    # cur.close()
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    sqlcommand = f'''select STUDENT.first_name,STUDENT.last_name,STUDENT.roll_no,STUDENT.phone,STUDENT.email,warden.warden_email,warden.name from STUDENT join warden on warden.warden_id=STUDENT.warden_id_id and STUDENT.id="{x}"'''
    # sqlcommand='select first_name,last_name,roll_no,phone,email,warden_email,name from STUDENT,warden where STUDENT.warden_id_id=warden.warden_id and id=x'
    cur.execute(sqlcommand)
    u = []
    for i in cur:
        u.append(i) 
    res1 = list(map(itemgetter(0), u))
    res2 = list(map(itemgetter(1), u))
    res3 = list(map(itemgetter(2), u))
    res4 = list(map(itemgetter(3), u))
    res5 = list(map(itemgetter(4), u))
    res6 = list(map(itemgetter(5), u))
    res7 = list(map(itemgetter(6), u))
    ins = record()
    ins.fname = res1[0]
    ins.lname = res2[0]
    ins.roll_no = res3[0]
    ins.phone = res4[0]
    ins.student_email = res5[0]
    ins.warden_email = res6[0]
    ins.warden_name = res7[0]
    ins.date_of_entry = str(d1)
    ins.time_of_entry = current_time
    ins.save()
    mess = f'Hello, {ins.fname}{ins.lname}\n YOU HAVE SUCCESSFULLY MADE YOUR ENTRY\n DATE OF ENTRY:{ins.date_of_entry}\n TIME OF ENTRY:{ins.time_of_entry}\n Thanks!!'
    subject = 'SUCCESSFUL NIGHT ENTRY!!!'
    sendfrom = settings.EMAIL_HOST_USER
    toaddress = [ins.student_email]
    send_mail(subject, mess, sendfrom, toaddress, fail_silently=False)
    # return render(req, 'index.html')
    messages.success(req,"SCANNED SUCCESSFULLY!!THANK YOU")
    return render(req, 'index_div.html')


def display(req):
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    waremail=req.session['email'] 
    sqlcommand11=f'''select warden_id from warden where warden_email="{waremail}"'''
    cur.execute(sqlcommand11)
    val=cur.fetchall()
    res9 = list(map(itemgetter(0), val))
    warid=res9[0]
    print(warid)
    cur.close()
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    sqlcommand2 = f'''select fname,lname,roll_no,date_of_entry,time_of_entry from Record_Table where warden_email="{waremail}"'''
    cur.execute(sqlcommand2)
    results = cur.fetchall()
    cur.close()
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    sqlcommand = f'select first_name,last_name from STUDENT where warden_id_id="{warid}"'
    cur.execute(sqlcommand)
    u = []
    for i in cur:
        u.append(i)
    cur.close()
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    y = datetime.datetime.now()
    d1 = y.strftime("%Y-%m-%d")
    print(d1)
    sqlcommand1 = f'''select fname,lname from Record_Table where date_of_entry="{d1}" and warden_email="{waremail}"'''
    cur.execute(sqlcommand1)
    a = []
    for i in cur:
        a.append(i)
    res1 = list(map(itemgetter(0), u))
    res2 = list(map(itemgetter(1), u))
    res3 = list(map(itemgetter(0), a))
    res4 = list(map(itemgetter(1), a))
    print(res3)
    print(res4)
    # stringList1 = ' '.join([str(item) for item in res3 ])
    # stringList2 = ' '.join([str(item) for item in res4 ])
    # list(stringList1)
    # print(stringList1)
    # stringList1.extend(stringList2)
    # stringList1[0: ] = [''.join(stringList1[0 ])]
    # res1.extend(res2)
    # res1[0: ] = [''.join(res1[0 ])]
    # print(res1)
    # print(stringList1)   
    f = []
    l = []
    i = 0
    k = len(res1)
    while i < k:
        if res1[i] not in res3 or res2[i] not in res4:
            f.append(res1[i])
            l.append(res2[i])
        i += 1
    names = [i + j for i, j in zip(f, l)]
    return render(req, 'display.html', {'names': names, 'results': results})


def generate(req):
    if req.session.get('username'):
        # print(username)
        username = req.session['username']
        obj = CustomUser.objects.get(username=username)
        name = f'''WELCOME {username}!!
        SCAN YOUR QR-CODE TO MAKE YOUR ENTRY'''
        context = {
            'name': name,
            'obj': obj,
        }
        return render(req, 'index.html', context)
    messages.error(req, 'YOU ARE LOGGED OUT!!')
    return redirect('login')


def start(req):
    return render(req, 'start.html')


#def welcome(req):
#    return render(req, 'welcome.html')


def login(req):
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    sqlcommand = 'select username,password from STUDENT'
    cur.execute(sqlcommand)
    u = []
    for i in cur:
        u.append(i)
        ##list of tuples
    res = list(map(itemgetter(0), u)) #usernames
    res2 = list(map(itemgetter(1), u)) #passwords
    print(u)
    print(res)
    print(res2)
    print(res[0])
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        i = 0
        k = len(res) #current users
        while i < k:
            if res[i] == username and res2[i] == password:
                obj1 = CustomUser.objects.get(username=username, password=password)
                if obj1.is_active == True:
                    req.session['username'] = username
                    return render(req, 'generate.html', {'username': username})
            i += 1
        else:
            messages.info(req, 'Check username or password entered')
            return redirect('login')

    return render(req, 'login.html')


# def pass_valid(passwd):
#     val=True
#     SpecialSym = ['$', '@', '#', '%']
#
#     if not any(char.isdigit() for char in passwd):
#        val=False
#        print('Password should have at least one numeral')
#     if not any(char.isupper() for char in passwd):
#         val = False
#         print('Password should have at least one uppercase letter')
#     if not any(char.islower() for char in passwd):
#         val = False
#         print('Password should have at least one lowercase letter')
#     if not any(char in SpecialSym for char in passwd):
#         val = False
#         print('Password should have at least one of the symbols $@#')
#     if not val:
#         return val
def register(req):
    if req.method == 'POST':
        get_otp = req.POST.get('otp', False)
        if get_otp:
            get_usr = req.POST['usr']
            usr = CustomUser.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(req, f'Account is created for {usr.username}')
                return redirect('login')
            else:
                messages.warning(req, 'You entered wrong OTP')
                return render(req, 'register.html', {'otp': True, 'usr': usr})
        print("hello")
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        username = req.POST['username']
        email = req.POST['email']
        roll_no = req.POST['roll_no']
        phone = req.POST['phone']
        gender = req.POST['show']
        Course = req.POST['dropdown']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']

        print(first_name, last_name, username)

        # conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
        # cur = conn.cursor()
        # sqlcommand = 'select id from warden where gender="male" or gender=="Male"'

        if password != confirm_password:
            messages.error(req, 'Confirm password must match entered password')
            print("match error")
            return redirect('/')

        elif not "@thapar.edu" in email:
            messages.warning(req, "Domain of email is not valid")
            print("domain error")
            return redirect('register')

        elif first_name == "" or last_name == "" or phone == "" or email == "" or username == "" or password == "" or gender == "" or roll_no == "":
            messages.error(req, 'All fields are mandatory')
            print("field error")
            return redirect('/')
        else:
            # conn = mcdb.connect(host='127.0.0.1', user='root', passwd='garg3404', database='STUDENT')
            # cur = conn.cursor()
            # sql='''INSERT INTO entry_system (first_name, last_name, username, email, phone, password)VALUES(first_name, last_name, username, email, phone, password)'''
            # cur.execute(sql)
            # conn.commit()
            # print("data saved")
            usr = CustomUser(first_name=first_name, last_name=last_name, confirm_password=confirm_password,
                             username=username, roll_no=roll_no, email=email, phone=phone, password=password,
                             gender=gender, Course=Course)
            obj = User.objects.get(gender=gender)
            usr.warden_id = obj
            usr.is_active = False
            usr.save()
            otp1 = random.randint(100000, 999999)
            print(otp1)
            UserOTP.objects.create(user=usr, otp=otp1)
            mess = f'Hello, {usr.first_name},\nYour OTP is {otp1}\n Thanks!!'
            subject = 'WELCOME! TO NIGHT PORTAL SYSTEM-PLEASE VERIFY YOUR EMAIL'
            #  message = f'''{first_name} {last_name} you successfully registered yourself on 'NIGHT ENTRY PORTAL' with USERNAME:{username} and in 'otp section' fill {otp1}'''
            sendfrom = settings.EMAIL_HOST_USER
            toaddress = [usr.email]
            send_mail(subject, mess, sendfrom, toaddress, fail_silently=False)
            #  otp=otp1
            #  print("data saved")
            return render(req, 'register.html', {'otp': True, 'usr': usr})
    # Create your views here.
    return render(req, 'register.html')


def login_warden(req):
    conn = mcdb.connect(host='localhost', user='root', passwd='garg3404', database='project_nps')
    cur = conn.cursor()
    sqlcommand = 'select warden_email,password from warden'
    cur.execute(sqlcommand)
    w = []
    for i in cur:
        w.append(i)
    res = list(map(itemgetter(0), w))
    res2 = list(map(itemgetter(1), w))
    if req.method == 'POST':
        warden_email = req.POST['email']
        password = req.POST['password']
        i = 0
        k = len(res)
        while i < k:
            if res[i] == warden_email and res2[i] == password:
               
                req.session['email'] = warden_email
                return render(req, 'index_div.html', {'email': warden_email})
            i += 1
        else:
            messages.info(req, 'check email or password')
            return render(req, 'login_div.html')

    return render(req, 'login_div.html')


def register_warden(req):
    if req.method == "POST":
        user = User()
        user.name = req.POST['Uname']
        user.gender = req.POST['gender']
        user.warden_email = req.POST['email']
        user.password = req.POST['password']
        if user.name == "" or user.gender == "" or user.warden_email == "" or user.password == "":
            messages.info(req, 'you are required to fill all the fields')
            return redirect('register_warden')
        else:
            user.save()

    return render(req, 'register_div.html')


def resetpage(req):
    return render(req, 'pass_reset.html')


def password_reset_request(req):
    if req.method == "POST":
        email = req.POST['email']
        if not "@thapar.edu" in email:
            messages.error(req, "Domain of email is not valid")
            print("domain error")
            return render(req, 'pass_reset.html')
        current_site = get_current_site(req)
        user = CustomUser.objects.get(email=email)
        print(user.first_name)
        if user:
            email_contents = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': PasswordResetTokenGenerator().make_token(user),
            }
            link = reverse('reset-user-password',
                           kwargs={'uidb64': email_contents['uid'], 'token': email_contents['token']})
            email_subject = 'Password reset Instructions'
            reset_url = 'http://' + current_site.domain + link
            email = EmailMessage(
                email_subject,
                'Hi,there! Please click the link below to reset your password\n' + reset_url,
                'noreply@semicolon.com',
                [email],
            )
            email.send(fail_silently=False)
            messages.success(req, 'We have sent you an email to reset your password')
    return render(req, 'pass_reset.html')


class CompletePasswordReset(View):
    def get(self, req, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(req, 'Password reset link is invalid,please request a new one')
                return render(req, 'pass_reset.html', context)

        except Exception as identifier:
            pass
        return render(req, 'set-new-password.html', context)

    def post(self, req, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        if req.method == "POST":
            password = req.POST['password']
            password2 = req.POST['password2']
            if password != password2:
                messages.error(req, 'Passwords do not match')
                return render(req, 'set-new-password.html', context)
            try:
                user_id = force_text(urlsafe_base64_decode(uidb64))
                user = CustomUser.objects.get(id=user_id)
                user.password = password
                user.confirm_password=password
                user.save()
                messages.success(req, 'Password reset successfully')
                return redirect('login')

            except Exception as identifier:
                import pdb
                pdb.set_trace()
                messages.info(req, 'Something went wrong,try again!!')
                return render(req, 'set-new-password.html', context)


def logout(req):
    auth.logout(req)
    messages.success(req, 'You have been successfully logged out')
    return redirect('login')

def logout1(req):
    auth.logout(req)
    messages.success(req, 'You have been successfully logged out')
    return redirect('login_warden')
def cal(req):
    # print(calendar.weekheader(3)) sun mon.....
    # print(calendar.firstweekday());

    year=timezone.now().year
    # print(calendar.calendar(year))
    l=[]
    for i in range(1,13):
        cal=HTMLCalendar().formatmonth(year,i)
        l.append(cal)
    return render(req,'calendar.html',{"cal":l,})
    # return HttpResponse("hi");

# Create your views here.
