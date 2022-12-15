''' Cuthbert Musengi +263778241753'''

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from datetime import date


# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fullname']
        em = request.POST['email']
        m = request.POST['mobile']
        s = request.POST['subject']
        msg = request.POST['message']
        try:

            Contact.objects.create(fullname=f, email=em, mobile=m, subject=s, message=msg, msgdate=date.today(),
                                   isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())


def signup(request):
    error=""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']

        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user, contact=c,role=r)
            error="no"
        except:
            error="yes"
    return render(request,'signup.html', locals())

def userlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'login.html', locals())


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)


    d = {'data':data,'user':user}
    return render(request,'profile.html',d)

def upload_cv(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':

        s = request.POST['subject']
        n = request.FILES['cvfile']
        f = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Cv.objects.create(user=u,uploadingdate=date.today(),subject=s,cvfile=n,
                                 filetype=f,description=d,status='pending')
            error="no"
        except:
            error="yes"
    return render(request,'upload_cv.html', locals())


def view_mycv(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    cv = Cv.objects.filter(user = user)

    d = {'cv':cv}
    return render(request,'view_mycv.html',d)

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error ="yes"
        except:
            error = "yes"
    return render(request,'admin_login.html', locals())

def admin_home(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    pn = Cv.objects.filter(status="pending").count()
    an = Cv.objects.filter(status="Accept").count()
    rn = Cv.objects.filter(status="Reject").count()
    alln = Cv.objects.all().count()
    d = {'pn':pn,'an':an,'rn':rn,'alln':alln}
    return render(request,'admin_home.html',d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    users = Signup.objects.all()

    d = {'users':users}
    return render(request,'view_users.html',d)

def pending_resume(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    resume = Cv.objects.filter(status = "pending")
    d = {'resume':resume}
    return render(request, 'pending_resume.html',d)

def promoted_cv(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    resume = Cv.objects.filter(status = "Promoted")
    d = {'resume':resume}
    return render(request, 'promoted_cv.html',d)

def rejected_cv(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    resume = Cv.objects.filter(status = "Reject")
    d = {'resume':resume}
    return render(request, 'rejected_cv.html',d)



def assign_promotion(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    resume = Cv.objects.get(id=pid)
    error = ""
    if request.method=='POST':
        s = request.POST['status']
        try:
            resume.status = s
            resume.save()
            error="no"
        except:
            error="yes"
    d = {'resume':resume,'error':error}
    return render(request, 'assign_promotion.html',d)

def all_cv(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    resume = Cv.objects.all()
    d = {'resume':resume}
    return render(request, 'all_cv.html',d)

def delete_mycv(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    resume = Cv.objects.get(id=pid)
    resume.delete()
    return redirect('view_mycv')

def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')

def delete_cv(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    resume = Cv.objects.get(id=pid)
    resume.delete()
    return  redirect('all_cv')


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    error = False
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']

        user.first_name = f
        user.last_name = l
        data.contact = c

        user.save()
        data.save()
        error=True

    d = {'data':data,'user':user,'error':error}
    return render(request,'edit_profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"

    return render(request,'changepassword.html', locals())


def Logout(request):
    logout(request)
    return redirect('index')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        try:
            if user.check_password(o):
                user.set_password(n)

                user.save()

                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'change_passwordadmin.html', locals())

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

