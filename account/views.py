from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import User
from .form import Userregisterform,Userloginform
from django.urls import reverse
def register(request):
    if request.method=="POST":
        userform=Userregisterform(request.POST)
        if userform.is_valid():
            username=userform.cleaned_data['username']
            password=userform.cleaned_data['password']
            passwordagain=userform.cleaned_data['passwordagain']
            email=userform.cleaned_data['email']
            if password==passwordagain:
                if User.objects.filter(username=username):
                    userform.add_error(None, "该用户名已被注册")
                else:
                    User.objects.create(username=username,password=password,email=email)
                    return HttpResponseRedirect(reverse('login'))
            else:
                userform.add_error(None,"两次密码输入不一致")
    else:
        userform=Userregisterform()
    context = {}
    context['register_form'] = userform
    return render(request, 'register.html', context)
def login(request):
    if request.method=="POST":
        loginform=Userloginform(request.POST)
        if loginform.is_valid():
            username=loginform.cleaned_data['username']
            password=loginform.cleaned_data['password']
            user=User.objects.get(username=username)
            if user.password==password:
                request.session['username']=username
                i = request.session.get('username', default=None)
                return render(request,'index.html',{'username':i})
            else:
                loginform.add_error(None,"用户名或密码错误")
    else:
        loginform=Userloginform()
    context={}
    context['login_form']=loginform
    return render(request,'login.html',context)
def logout(request):
    if request.session.get('username',default=None):
        del request.session['username']
        return HttpResponse("您已登出")
    else:
       return redirect(reverse('login'))






# Create your views here.
