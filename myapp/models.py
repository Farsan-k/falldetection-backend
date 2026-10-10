from django.db import models

# Create your models here.
class Login(models.Model):
    Username=models.CharField(max_length=100)
    Password=models.CharField(max_length=100)
    Type=models.CharField(max_length=100)

class Doctor(models.Model):
    Name=models.CharField(max_length=100)
    Email=models.CharField(max_length=100)
    Phone=models.BigIntegerField()
    Photo=models.CharField(max_length=300)
    Qualification=models.CharField(max_length=100)
    Department=models.CharField(max_length=100)
    Gender=models.CharField(max_length=100)
    DOB=models.DateField()
    Place=models.CharField(max_length=100)
    City=models.CharField(max_length=100)
    State=models.CharField(max_length=100)
    Pincode=models.CharField(max_length=100)
    Status=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE,default=1)

class User(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone = models.BigIntegerField()
    Photo = models.CharField(max_length=100)
    Gender = models.CharField(max_length=100)
    Place = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Pincode = models.CharField(max_length=100)
    DOB = models.DateField()
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Complaint(models.Model):
    Date=models.DateField()
    Complaint=models.CharField(max_length=100)
    Replay=models.CharField(max_length=100)
    Status=models.CharField(max_length=100)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)

class Review(models.Model):
    Review=models.CharField(max_length=100)
    Date=models.DateField()
    USER = models.ForeignKey(User, on_delete=models.CASCADE)

class Schedule(models.Model):
    Date=models.DateField()
    Fromtime=models.CharField(max_length=100)
    Totime=models.CharField(max_length=100)
    Status=models.CharField(max_length=100)
    DOCTOR = models.ForeignKey(Doctor, on_delete=models.CASCADE,default=1)

class Booking(models.Model):
    Date=models.DateField()
    Status = models.CharField(max_length=100)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    SCHEDULE= models.ForeignKey(Schedule, on_delete=models.CASCADE)

class Chat(models.Model):
    Messege=models.CharField(max_length=100)
    Date=models.DateField()
    FROMID=models.ForeignKey(Login,on_delete=models.CASCADE,related_name="fromid")
    TOID=models.ForeignKey(Login,on_delete=models.CASCADE,related_name="toid")




class Patient(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone = models.BigIntegerField()
    Photo = models.CharField(max_length=100)
    Gender = models.CharField(max_length=100)
    Place = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Pincode = models.CharField(max_length=100)
    DOB = models.DateField()
    State = models.CharField(max_length=100)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)


class Notification(models.Model):
    Date=models.DateField()
    Notification=models.CharField(max_length=100)
    Photo = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    PATIENT= models.ForeignKey(Patient, on_delete=models.CASCADE)

