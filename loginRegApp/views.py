from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    errorsFromValidator = User.objects.registrationValidator(request.POST)
    print("********", errorsFromValidator)
    if len(errorsFromValidator) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")

    encryptedPw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()

    newuser = User.objects.create(firstName = request.POST['fname'], lastName= request.POST['lname'] , email = request.POST['email'] , password = encryptedPw , birthday = request.POST['birthday'])

    request.session['loggedInUserId']= newuser.id


    return redirect("/newsFeed")

def newsFeed(request):
    if 'loggedInUserId' not in request.session:
        messages.error(request, "You must be logged in to view the news feed")
        return redirect("/")

    context = {
        'loggedinUser': User.objects.get(id= request.session['loggedInUserId']),
        'allevents': Event.objects.all()
    }

    return render(request, "newsfeed.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    print(request.POST)
    errorsFromValidator= User.objects.loginValidator(request.POST)
    print("********PRINTING THE LOGIN ERRORS",errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    
    matchingemail = User.objects.filter(email = request.POST['email'] )
    request.session['loggedInUserId']= matchingemail[0].id

    return redirect("/newsFeed")

def createEvent(request):
    print(request.POST)

    errorsFromValidator = Event.objects.eventCreateValidator(request.POST)

    print("ERRORS FROM VALIDATOR", errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/newsFeed")


    newevent = Event.objects.create(name = request.POST['name'], description = request.POST['desc'], location = request.POST['location'], startTime = request.POST['start'],endTime = request.POST['end'], planner= User.objects.get(id=request.session['loggedInUserId']))
    User.objects.get(id=request.session['loggedInUserId']).eventsToAttend.add(newevent)
    return redirect("/newsFeed")


def showEvent(request, eventID):

    context = {
        "eventObj": Event.objects.get(id=eventID),
        'loggedinuser': User.objects.get(id=request.session['loggedInUserId'])
    }
    return render(request, "eventInfo.html", context)

def cancelEvent(request, eventID):
    e = Event.objects.get(id=eventID)
    e.delete()

    return redirect("/newsFeed")

def updateEvent(request, eventID):
    e = Event.objects.get(id= eventID)
    e.name = request.POST['name']
    e.description = request.POST['desc']
    e.location = request.POST['location']
    e.startTime = request.POST['start']
    e.endTime = request.POST['end']
    e.save()
    return redirect("/newsFeed")

def userDetails(request, userid):
    context = {
        'specificuser': User.objects.get(id= userid)
    }
    return render(request, "userdetails.html", context)