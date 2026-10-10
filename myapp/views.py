import os
import base64
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from myapp.models import *


def admin_home(request):
    return render(request, 'admin/homeindex.html')


def admin_changepassword(request):
    return render(request, 'admin/Change password.html')


def admin_changepassword_post(request):
    currentpassword = request.POST['textfield']
    Newpassword = request.POST['textfield2']
    Confirmpassword = request.POST['textfield3']
    l = Login.objects.filter(id=request.session['lid'], Password=currentpassword)
    if l.exists():
        if Newpassword == Confirmpassword:
            l = Login.objects.filter(id=request.session['lid'], Password=currentpassword).update(
                Password=Confirmpassword)
            return HttpResponse('''<script>alert("Password updated");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert("Password dose not match");window.location='/myapp/admin_changepassword/'</script>''')
    else:
        return HttpResponse(
            '''<script>alert("Invalid password");window.location='/myapp/admin_changepassword/'</script>''')


def login(request):
    return render(request, 'loginindex.html')


def login_post(request):
    Username = request.POST['textfield']
    Password = request.POST['textfield2']
    l = Login.objects.filter(Username=Username, Password=Password)
    if l.exists():
        ll = Login.objects.get(Username=Username, Password=Password)
        request.session['lid'] = ll.id
        if ll.Type == 'admin':
            return HttpResponse('''<script>alert("Login sucssesfully");window.location='/myapp/admin_home/'</script>''')
        elif ll.Type == 'Doctor':
            return HttpResponse(
                '''<script>alert("Login sucssesfully");window.location='/myapp/doctor_home/'</script>''')
        else:
            return HttpResponse('''<script>alert("User not found");window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert("Wrong password");window.location='/myapp/login/'</script>''')


def admin_sendreply(request, id):
    return render(request, 'admin/send reply.html', {'id': id})


def admin_sendreply_post(request):
    Reply = request.POST['textfield']
    id = request.POST['id']
    Complaint.objects.filter(id=id).update(Replay=Reply, Status='replied')
    return HttpResponse('''<script>alert("Replied");window.location='/myapp/admin_viewcomplaint/'</script>''')


def admin_viewdoctor(request):
    re = Doctor.objects.filter(Status='pending')
    return render(request, 'admin/View doctor.html', {'data': re})


def admin_viewdoctor_post(request):
    Search = request.POST['textfield']
    re = Doctor.objects.filter(Status='pending', Name__icontains=Search)
    return render(request, 'admin/View doctor.html', {'data': re})


def approve_doctor(request, id):
    Doctor.objects.filter(LOGIN_id=id).update(Status='Approve')
    Login.objects.filter(id=id).update(Type='Doctor')
    return HttpResponse('''<script>alert("Approved");window.location='/myapp/admin_viewdoctor/'</script>''')


def reject_doctor(request, id):
    Doctor.objects.filter(LOGIN_id=id).update(Status='Reject')
    Login.objects.filter(id=id).update(Type='Reject')
    return HttpResponse('''<script>alert("Reject");window.location='/myapp/admin_viewdoctor/'</script>''')


def admin_viewapproveddoctor(request):
    re = Doctor.objects.filter(Status='Approve')
    return render(request, 'admin/view approved doctor.html', {'data': re})


def admin_viewapproveddoctor_post(request):
    Search = request.POST['textfield']
    re = Doctor.objects.filter(Status='Approve', Name__icontains=Search)
    return render(request, 'admin/view approved doctor.html', {'data': re})


def admin_viewrejecteddoctor(request):
    re = Doctor.objects.filter(Status='Reject')
    return render(request, 'admin/view rejected doctor.html', {'data': re})


def admin_viewrejecteddoctor_post(request):
    Search = request.POST['textfield']
    re = Doctor.objects.filter(Status='Reject', Name__icontains=Search)
    return render(request, 'admin/view rejected doctor.html', {'data': re})


def admin_viewcomplaint(request):
    re = Complaint.objects.all()
    return render(request, 'admin/View complaint.html', {'data': re})


def admin_viewcomplaint_post(request):
    From = request.POST['textfield']
    To = request.POST['textfield2']
    re = Complaint.objects.filter(Date__range=[From, To])
    return render(request, 'admin/View complaint.html', {'data': re})


def admin_viewreview(request):
    re = Review.objects.all()
    return render(request, 'admin/View review.html', {'data': re})


def admin_viewreview_post(request):
    From = request.POST['textfield']
    To = request.POST['textfield2']
    re = Review.objects.filter(Date__range=[From, To])
    return render(request, 'admin/View review.html', {'data': re})


def admin_viewuser(request):
    re = User.objects.all()
    return render(request, 'admin/View user.html', {'data': re})


def admin_viewuser_post(request):
    Search = request.POST['textfield']
    re = User.objects.filter(Name__icontains=Search)
    return render(request, 'admin/View user.html', {'data': re})


def doctor_home(request):
    return render(request, 'doctor/doctorindex.html')


def doctor_changepassword(request):
    return render(request, 'doctor/Change password.html')


def doctor_changepassword_post(request):
    Currentpassword = request.POST['textfield']
    Newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    l = Login.objects.filter(id=request.session['lid'], Password=Currentpassword)
    if l.exists():
        if Newpassword == confirmpassword:
            l = Login.objects.filter(id=request.session['lid'], Password=Currentpassword).update(
                Password=confirmpassword)
            return HttpResponse('''<script>alert("Password updated");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert("Password dose not match");window.location='/myapp/admin_changepassword/'</script>''')
    else:
        return HttpResponse(
            '''<script>alert("Invalid password");window.location='/myapp/admin_changepassword/'</script>''')


def doctor_doctor(request):
    return render(request, 'doctor/regindex.html')


def doctor_doctor_post(request):
    Name = request.POST['textfield']
    Email = request.POST['textfield2']
    Phone = request.POST['textfield3']

    Photo = request.FILES['fileField']
    f=FileSystemStorage()
    d=datetime.now().strftime('%Y%m%d-%H%M%S')+".jpg"
    f.save(d,Photo)
    path=f.url(d)

    Qualification = request.POST['select']
    Department = request.POST['select2']
    Gender = request.POST['gender']
    DOB = request.POST['textfield8']
    print(DOB)
    Place = request.POST['textfield4']
    City = request.POST['City']
    State = request.POST['textfield6']
    Pincode = request.POST['textfield7']
    password = request.POST['textfield9']
    confirmpassword = request.POST['textfield10']


    l=Login()
    l.Username=Email
    l.Password=password
    l.Type='doctor'
    l.save()

    d=Doctor()
    d.Name=Name
    d.Phone=Phone
    d.Photo=path
    d.Qualification=Qualification
    d.Department=Department
    d.Gender=Gender
    d.DOB=DOB
    d.Place=Place
    d.City=City
    d.Email=Email
    d.State=State
    d.Pincode=Pincode
    d.Status='pending'
    d.LOGIN=l

    d.save()
    return HttpResponse('''<script>alert("success");window.location='/myapp/login/'</script>''')


def doctor_editdoctor(request,id):
    t=Doctor.objects.get(id=id)

    return render(request, 'doctor/edit doctor.html',{"data":t})


def doctor_editdoctor_post(request):
    Name = request.POST['textfield']
    Email = request.POST['textfield2']
    Phone = request.POST['textfield3']
    id = request.POST['id']

    d=Doctor.objects.get(id=id)


    if 'fileField' in request.FILES:
        Photo = request.FILES['fileField']
        if Photo !='':
            f=FileSystemStorage()
            date=datetime.now().strftime('%Y%m%d-%H%M%S')+".jpg"
            f.save(d,Photo)
            path=f.url(date)
            d.Photo = path
            d.save()

    Qualification = request.POST['select']
    Department = request.POST['select2']
    Gender = request.POST['RadioGroup1']
    DOB = request.POST['textfield8']
    Place = request.POST['textfield4']
    City = request.POST['textfield5']
    State = request.POST['textfield6']
    Pincode = request.POST['textfield7']


    d.Name=Name
    d.Phone=Phone
    d.Qualification=Qualification
    d.Department=Department
    d.Gender=Gender
    d.DOB=DOB
    d.Place=Place
    d.City=City
    d.Email=Email
    d.State=State
    d.Pincode=Pincode
    d.save()
    return HttpResponse('''<script>alert("success");window.location='/myapp/doctodoctor_viewprofile/'</script>''')



def doctor_editschedule(request,id):
    f=Schedule.objects.get(id=id)
    return render(request, 'doctor/edit schedule.html',{'data':f})


def doctor_editschedule_post(request):
    Date = request.POST['textfield']
    Fromtime = request.POST['textfield2']
    Totime = request.POST['textfield3']
    id=request.POST['id']

    ff=Schedule.objects.get(id=id)
    ff.Date = Date
    ff.Fromtime = Fromtime
    ff.Totime = Totime
    ff.save()
    return HttpResponse('''<script>alert("Edited ");window.location='/myapp/doctor_viewschedule/'</script>''')



def doctor_manageschedule(request):
    return render(request, 'doctor/manage schedule.html')


def doctor_manageschedule_post(request):
    Date = request.POST['textfield']
    Fromtime = request.POST['textfield2']
    Totime = request.POST['textfield3']

    a=Schedule()
    a.Date=Date
    a.Fromtime=Fromtime
    a.Totime=Totime
    a.DOCTOR=Doctor.objects.get(LOGIN_id=request.session['lid'])
    a.save()
    return HttpResponse('''<script>alert("Scheduled ");window.location='/myapp/doctor_manageschedule/'</script>''')


def doctor_viewbooking(request,id):
    data=Booking.objects.filter(SCHEDULE_id=id)
    return render(request, 'doctor/view booking.html',{'data':data})


def doctor_viewbooking_post(request):
    fd = request.POST['textfield']
    td = request.POST['textfield2']
    data = Booking.objects.filter(SCHEDULE__DOCTOR__LOGIN_id=request.session['lid'], Date__range=[fd, td])
    return render(request, 'doctor/view booking.html', {'data': data})


def doctor_viewfall(request):
    lid = request.session['lid']
    data = Notification.objects.filter(
        PATIENT__USER__booking__SCHEDULE__DOCTOR__LOGIN_id=lid
    ).distinct()
    return render(request, 'doctor/View fall.html', {'data': data})


def doctor_viewfall_post(request):
    return HttpResponse("ok")


def doctor_viewpatient(request):
    p=Patient.objects.all()
    return render(request, 'doctor/View patient.html',{'data':p})


def doctor_viewpatient_post(request):
    se = request.POST['textfield']
    p = Patient.objects.filter(Name__icontains=se)
    return render(request, 'doctor/view patient.html', {'data': p})


def doctor_viewprofile(request):
    g=Doctor.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'doctor/View profile.html',{"data":g})


def doctor_viewprofile_post(request):

    return HttpResponse("ok")


def doctor_viewschedule(request):
    data=Schedule.objects.filter(DOCTOR__LOGIN_id=request.session['lid'])


    return render(request, 'doctor/View schedule.html', {'data': data})
def delete_schedule(request,id):
    Schedule.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Deleted");window.location='/myapp/doctor_viewschedule/'</script>''')

def doctor_viewschedule_post(request):
    fd = request.POST['textfield']
    td = request.POST['textfield2']
    data = Schedule.objects.filter(DOCTOR__LOGIN_id=request.session['lid'],Date__range=[fd,td])
    return render(request, 'doctor/View schedule.html', {'data': data})


def logout(request):
    request.session['lid']=''
    return HttpResponse('''<script>alert("logout");window.location='/myapp/login/'</script>''')

def forget_password(request):
    return render(request, 'forgetpassword.html')

def forget_password_post(request):
    email=request.POST['textfield']

    import smtplib, ssl

    import random

    p=random.randint(1000,100000)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "teameeey@gmail.com"  # Enter your address
    receiver_email = email # Enter receiver address
    # password = "pmxx bdki tlnz nehb"
    password = ("pmxx bdki tlnz nehb")
    message = "Your new password is "+ str(p)


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


    Login.objects.filter(Username=email).update(Password=str(p))





    return HttpResponse("<script>alert('Password resets');window.location='/myapp/login/'</script>")

#===========Chat===============================


def chat1(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = Patient.objects.get(id=cid)
    # qry = Patient.objects.get(USER__LOGIN_id=cid).distinct

    return render(request, "doctor/Chat.html", {'photo': qry.Photo, 'name': qry.Name, 'toid': cid})

def chat_view(request):
    fromid = request.session["lid"]
    id = request.session["userid"]
    toid=Patient.objects.get(id=id).USER.LOGIN.id
    request.session["tolid"]=toid
    qry = Patient.objects.get(id=request.session["userid"])
    # qry = Patient.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.Messege, "to": i.TOID_id, "date": i.Date, "from": i.FROMID_id})

    return JsonResponse({'photo': qry.Photo, "data": l, 'name': qry.Name, 'toid': request.session["tolid"]})

def chat_send(request, msg):
    lid = request.session["lid"]
    id = request.session["userid"]
    toid = Patient.objects.get(id=id).USER.LOGIN.id
    # toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.Messege = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.Date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})






#=================User=======================

def User_registration(request):
    Name=request.POST['name']
    Email=request.POST['email']
    Phone=request.POST['phone']
    Photo=request.POST['photo']
    Gender=request.POST['gender']
    Place=request.POST['place']
    City=request.POST['city']
    State=request.POST['state']
    Pincode=request.POST['pincode']
    DOB=request.POST['DOB']
    Password=request.POST['password']
    Confiempassword=request.POST['Confirmpassword']

    date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    dcode=base64.b64decode(Photo)
    fs = open(os.path.join(settings.MEDIA_ROOT, 'User', date), "wb")
    fs.write(dcode)
    fs.close()

    l=Login()
    l.Username=Email
    l.Password=Confiempassword
    l.Type="User"
    l.save()

    us=User()
    us.Name=Name
    us.Email=Email
    us.Phone=Phone
    us.Photo="/media/User/"+date
    us.Gender=Gender
    us.Place=Place
    us.City=City
    us.State=State
    us.Pincode=Pincode
    us.DOB=DOB
    us.LOGIN=l
    us.save()
    return JsonResponse({'status':'ok'})

def User_login(request):
    Username=request.POST['Username']
    Password=request.POST['Password']
    l = Login.objects.filter(Username=Username, Password=Password)
    if l.exists():
        ll = Login.objects.get(Username=Username, Password=Password)
        lid = ll.id
        if ll.Type == 'User':
            data=User.objects.get(LOGIN_id=lid)
            return JsonResponse({'status': 'ok','lid':str(lid),'name':data.Name,'photo':data.Photo})

        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status':'no'})

def User_chagepassword(request):
    Currentpassword = request.POST['Currentpassword']
    Newpassword = request.POST['Newpassword']
    confirmpassword = request.POST['confirmpassword']
    lid = request.POST['lid']
    l = Login.objects.filter(id=request.POST['lid'], Password=Currentpassword)
    if l.exists():
        if Newpassword == confirmpassword:
            l = Login.objects.filter(id=request.POST['lid'], Password=Currentpassword).update(Password=confirmpassword)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status':'no'})

def User_viewprofile(request):
    lid=request.POST['lid']
    up=User.objects.get(LOGIN_id=lid)
    return JsonResponse({'status':'ok',
                         'name':up.Name,
                         'email':up.Email,
                         'phone':up.Phone,
                         'photo':up.Photo,
                         'gender':up.Gender,
                         'place':up.Place,
                         'city':up.City,
                         'state':up.State,
                         'pincode':up.Pincode,
                         'DOB':up.DOB,
                         })

def User_editprofile(request):
    Name=request.POST['name']
    Email=request.POST['email']
    Phone=request.POST['phone']
    Photo=request.POST['photo']
    Gender=request.POST['gender']
    Place=request.POST['place']
    City=request.POST['city']
    State=request.POST['state']
    Pincode=request.POST['pin']
    DOB=request.POST['DOB']
    lid=request.POST['lid']

    u=User.objects.get(LOGIN_id=lid)

    if len(Photo)>0:

        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        dcode=base64.b64decode(Photo)
        fs = open(os.path.join(settings.MEDIA_ROOT, 'User', date), "wb")
        fs.write(dcode)
        fs.close()
        u.Photo = "/media/User/"+date
        u.save()

    u.Name=Name
    u.Email=Email
    u.Phone=Phone
    u.Gender=Gender
    u.Place=Place
    u.City=City
    u.State=State
    u.Pincode=Pincode
    u.DOB=DOB
    u.save()



    return JsonResponse({'status':'ok'})




def User_managepatient(request):
    Name=request.POST['name']
    Email=request.POST['email']
    Phone=request.POST['phone']
    Photo=request.POST['photo']
    Gender=request.POST['gender']
    Place=request.POST['place']
    City=request.POST['city']
    Pincode=request.POST['pincode']
    DOB=request.POST['dob']
    State=request.POST['state']
    lid=request.POST['lid']



    date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    dcode = base64.b64decode(Photo)
    fs = open(os.path.join(settings.MEDIA_ROOT, 'User', date), "wb")
    fs.write(dcode)
    fs.close()

    mp=Patient()
    mp.Name=Name
    mp.Email=Email
    mp.Phone=Phone
    mp.Photo="/media/User/"+date
    mp.Gender=Gender
    mp.Place=Place
    mp.City=City
    mp.Pincode=Pincode
    mp.DOB=DOB
    mp.State=State
    mp.USER=User.objects.get(LOGIN_id=lid)
    mp.save()
    return JsonResponse({'status':'ok'})


def User_viewpatient(request):
    lid=request.POST['lid']
    data = Patient.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in data:
        l.append({"name": i.Name,
                  "id": i.id,
                  "email": i.Email,
                  "phone": i.Phone,
                  "photo": i.Photo,
                  "gender": i.Gender,
                  "place": i.Place,
                  "city": i.City,
                  "pincode": i.Pincode,
                  "DOB": i.DOB,
                  "state": i.State,



                  })

    return JsonResponse({'status':'ok','data':l})




def User_editpatient_get(request):
    id=request.POST['sid']
    i = Patient.objects.get(id=id)

    return JsonResponse({'status':'ok',
                         "name": i.Name,
                  "email": i.Email,
                  "phone": i.Phone,
                  "photo": i.Photo,
                  "gender": i.Gender,
                  "place": i.Place,
                  "city": i.City,
                  "pincode": i.Pincode,
                  "DOB": i.DOB,
                  "state": i.State,})




def User_editpatient(request):
    Name = request.POST['name']
    Email = request.POST['email']
    Phone = request.POST['phone']
    Photo = request.POST['photo']
    Gender = request.POST['gender']
    Place = request.POST['place']
    City = request.POST['city']
    Pincode = request.POST['pincode']
    DOB = request.POST['DOB']
    State = request.POST['state']
    id = request.POST['id']
    mp = Patient.objects.get(id=id)

    if len(Photo)>0:


        date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        dcode = base64.b64decode(Photo)
        fs = open(os.path.join(settings.MEDIA_ROOT, 'User', date), "wb")
        fs.write(dcode)
        fs.close()
        mp.Photo = "/media/User/" + date
        mp.save()

    mp.Name = Name
    mp.Email = Email
    mp.Phone = Phone
    mp.Gender = Gender
    mp.Place = Place
    mp.City = City
    mp.Pincode = Pincode
    mp.DOB = DOB
    mp.State = State
    mp.save()


    return JsonResponse({'status':'ok'})



def User_deletepatient(request):
    pid=request.POST['pid']
    print(pid,'farsan')
    Patient.objects.get(id=pid).delete()
    return JsonResponse({'status':'ok'})





def User_viewfallnotifiction(request):
    lid=request.POST['lid']
    data=Notification.objects.filter(PATIENT__USER__LOGIN_id=lid)
    # data=Notification.objects.all()
    l=[]
    for i in data:
        l.append({"date":i.Date,
                  "notification":i.Notification,
                  "pname":i.PATIENT.Name,})
        print(l)

    return JsonResponse({'status':'ok','data':l})


def User_viewschedule(request):
    did=request.POST['did']

    print(did)
    data= Schedule.objects.filter(DOCTOR_id=did)
    l=[]
    for i in data :
        l.append({
            "id": i.id,
            "date":i.Date,
            "fromtime":i.Fromtime,
            "totime":i.Totime,
        })
    print(l)
    return JsonResponse({'status':'ok','data':l})


def User_viewbooking(request):
    lid = request.POST['lid']
    data = Booking.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in data:
        l.append({"date": i.SCHEDULE.Date,"Fromtime":i.SCHEDULE.Fromtime, "Totime":i.SCHEDULE.Totime ,'name':i.SCHEDULE.DOCTOR.Name,'Department':i.SCHEDULE.DOCTOR.Department ,'Place':i.SCHEDULE.DOCTOR.Place })

    return JsonResponse({'status':'ok','data':l})

def User_searchdoctor(request):
    # lid = request.POST['lid']
    data = Doctor.objects.filter(Status='Approve')
    l=[]
    for i in data:
        l.append({'name':i.Name,
                  'id':i.id,
                  'email':i.Email,
                  'phone':i.Phone,
                  'photo':i.Photo,
                  'qualification':i.Qualification,
                  'department':i.Department,
                  'gender':i.Gender,
                  'DOB':i.DOB,
                  'place':i.Place,
                  'city':i.City,
                  'state':i.State,
                  'pincode':i.Pincode,
                  'status':i.Status,
                  'dlid':i.LOGIN.id
                  })

    return JsonResponse({'status':'ok',"data":l})

def User_viewreply(request):
    lid = request.POST['lid']
    data = Complaint.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in data:
        l.append({'id': i.id,
                  'date': i.Date,
                  'Complaint': i.Complaint,
                  'Replay': i.Replay,
                  'status':i.Status,
                  })
    print(l)
    return JsonResponse({'status':'ok','data':l})

def User_sendcomplaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    obj=Complaint()
    obj.Date=datetime.now().today()
    obj.Complaint=complaint
    obj.Replay='pending'
    obj.Status='pending'
    obj.USER=User.objects.get(LOGIN_id=lid)
    obj.save()
    return JsonResponse({'status':'ok'})



def User_takeappointment(request):
    sid=request.POST['sid']
    lid=request.POST['lid']
    s=Booking()
    s.Date=datetime.now().today()
    s.Status='pending'
    s.SCHEDULE_id=sid
    s.USER=User.objects.get(LOGIN=lid)
    s.save()
    return JsonResponse({'status':'ok'})




def User_fall_notifiction(request):
    lid=request.POST['lid']
    nid=request.POST['nid']
    print(nid)
    from datetime import datetime,timedelta
    today = datetime.now().date()  # Today's date
    dd=Notification.objects.filter(PATIENT__USER__LOGIN_id=lid,id__gt=nid).order_by('id')
    if dd.exists():
        f=dd[0]
        print(f.id)
        return JsonResponse({"status":"ok",'nid':f.id,'message':'Fall is Detected..'})
    else:
        return JsonResponse({"status": "no"})



#=======chat================


def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.Messege=msg
    c.Date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.Messege, "from": i.FROMID_id, "date": i.Date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})


def api_report_fall(request):
    if request.method == 'POST':
        try:
            patient_id = request.POST.get('patient_id', '1')
            notification_text = request.POST.get('notification', 'fall is detected')

            p = Patient.objects.filter(id=patient_id)
            if not p.exists():
                p = Patient.objects.all()
                if not p.exists():
                    return JsonResponse({'status': 'error', 'message': 'No patient record found in database'})
            patient_obj = p.first()

            da = datetime.now().strftime("%Y%m%d%H%M%S%f") + ".jpg"
            photo_url = "/media/" + da
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            save_path = os.path.join(settings.MEDIA_ROOT, da)

            if 'photo' in request.FILES:
                with open(save_path, 'wb+') as destination:
                    for chunk in request.FILES['photo'].chunks():
                        destination.write(chunk)
            elif 'photo_base64' in request.POST:
                img_data = base64.b64decode(request.POST['photo_base64'])
                with open(save_path, 'wb') as f:
                    f.write(img_data)
            else:
                photo_url = ''

            today_date = datetime.now().date()
            cur_time = datetime.now().strftime("%H:%M:%S")
            notif = Notification.objects.create(
                Date=today_date,
                Notification=notification_text,
                PATIENT=patient_obj,
                Photo=photo_url,
                time=cur_time
            )
            return JsonResponse({'status': 'ok', 'id': notif.id, 'photo': photo_url})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'POST method required'})

