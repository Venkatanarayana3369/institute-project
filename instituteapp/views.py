from django.shortcuts import render,redirect,HttpResponse
from .models import courses
from .forms import registrationform
from .models import contact,feedbackdata
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth .decorators import login_required
import datetime as dt
date1=dt.datetime.now()


@login_required(login_url='login')
def homepage(request):
    return render (request,'homepage.html')

@login_required(login_url='login')
def contactpage(request):
    if request.method=="GET":
        return render (request,'contactpage.html')
    else:
        contact(
        name=request.POST['name'],
        email=request.POST['email'],
        mobile=request.POST['mobile'],
        course=request.POST['course'],
        location=request.POST['location'],
        ).save()
        return redirect('contact')

@login_required(login_url='login')
def servicepage(request):
    Courses=courses.objects.all()
    return render (request,'servicepage.html',{'courses':Courses})

@login_required(login_url='login')
def feedbackpage(request):
    if request.method=='GET':
        feedbacks=feedbackdata.objects.all().order_by("-id")
        return render (request,'feedbackpage.html',{'feedbacks':feedbacks})
    else:
        feedbackdata(
        content=request.POST['feedback'],
        date=date1
        ).save()
        feedbacks=feedbackdata.objects.all().order_by("-id")
        return render (request,'feedbackpage.html',{'feedbacks':feedbacks})

@login_required(login_url='login')
def gallerypage(request):
    return render (request,'gallerypage.html')


def loginpage(request):
    if request.method=='GET':
        return render(request,'loginpage.html')
    else:
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse('invalid username or password  ')

def logoutpage(request):
    logout(request)
    return redirect('login')

def registerpage(request):
    if request.method=='GET':
        form=registrationform()
        return render(request,'registerpage.html',{'form':form})
    else:
        form=registrationform(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user=user.set_password(user.password)
            return redirect ('login')
            form.save()
        else:
            return HttpResponse('Invalid Details')
