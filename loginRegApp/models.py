from django.db import models
from datetime import date, datetime
import bcrypt
import re

class UserManager(models.Manager):
    def registrationValidator(self, formInfo):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        today = date.today()
        # ClassName.objects.filter(field1="value for field1", etc.) - gets any records matching the query provided

        print("**********FILTERINGGGGGG", User.objects.filter(email = formInfo['email']))
        emailTaken = User.objects.filter(email = formInfo['email'])

        print("******")
        print(formInfo['birthday'])
        print(today)
        print("******")

        errors = {}
        if len(formInfo['fname']) == 0:
            errors['fnamereq'] = "First Name is required!"
        elif len(formInfo['fname']) < 2:
            errors['fnamelength'] = "First Name must be at least 2 characters!"

        if len(formInfo['lname']) == 0:
            errors['lnamereq'] = "Last Name is required!"

        if len(formInfo['email']) == 0:
            errors['emailreq'] = "email is required!"
        elif not EMAIL_REGEX.match(formInfo['email']):
            errors['invalidemail'] = "Email is not real, let's be real doe"
        elif len(emailTaken)>0:
            errors['emailtaken'] = "This email is already registered. Please try again"

        if len(formInfo['pw']) == 0:
            errors['pwReq'] = "Password is required!"
        elif len(formInfo['pw']) < 8:
            errors['pwlength'] = "Password must be at least 8 characters!"
        
        if formInfo['pw'] != formInfo['cpw']:
            errors['pwMatch'] = "Passwords must match!"

        if len(formInfo['birthday']) == 0:
            errors['bdayReq'] = "Birthday is required!"
        elif formInfo['birthday'] > str(today):
            errors['noFuturebday'] = "Birthday can't be in future!"
        

        return errors

    def loginValidator(self, formInfo):
        errors = {}
        matchingEmail = User.objects.filter(email=formInfo['email'])
        print("PRINTING MATCHING EMAIL HERE", matchingEmail)
        if len(matchingEmail) == 0:
            errors['emailnotfound'] = "This email is not found. Please register first."  

        elif not bcrypt.checkpw(formInfo['pw'].encode(), matchingEmail[0].password.encode()):
            errors['pwIncorrect'] = "Incorrect Password"

        # bcrypt.checkpw('test'.encode(), hash1.encode())


        return errors


class EventManager(models.Manager):
    def eventCreateValidator(self, formInfo):
        errors= {}
        now = datetime.now()
        if len(formInfo['name']) == 0:
            errors['nameReq'] = "Event Name Required"
        if len(formInfo['desc']) <10 :
            errors['descLength'] = "We need more details than that to create that event!"
        if len(formInfo['location']) == 0:
            errors['locationReq'] = "Event Location Required"
        if len(formInfo['start']) == 0:
            errors['startReq'] = "Start Time Required"
        elif formInfo['start'] < str(now):
            errors['noPastEvents']= "Event cannot be in the past"
        if len(formInfo['end']) == 0:
            errors['endReq'] = "End Time Required"
        elif formInfo['end'] < formInfo['start']:
            errors['invalidchoices'] = "Start time must be before end time"

        return errors

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    planner = models.ForeignKey(User, related_name="plannedEvents", on_delete= models.CASCADE)
    attendees = models.ManyToManyField(User, related_name= "eventsToAttend")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()

