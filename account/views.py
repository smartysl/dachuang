from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import User
from .form import Userregisterform,Userloginform,Changepasswordform
from django.urls import reverse
from django.core.mail import send_mail
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
            username=request.POST.get("username")
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
def changepassword(request):
    if request.session.get('username', default=None):
        if request.method == "POST":
            changepasswordform = Changepasswordform(request.POST)
            username = request.session['username']
            user = User.objects.get(username=username)
            password = user.password
            if changepasswordform.is_valid():
                if password == changepasswordform.cleaned_data['originalpassword']:
                    if changepasswordform.cleaned_data['newpassword'] == changepasswordform.cleaned_data[
                        'newpasswordagain']:
                        newpassword = changepasswordform.cleaned_data['newpassword']
                        user.password=newpassword
                        user.save()
                        return HttpResponseRedirect('login')
                    else:
                        changepasswordform.add_error(None, "两次密码输入不一致")
                else:
                    changepasswordform.add_error(None, "原密码输入错误")
        else:
            changepasswordform=Changepasswordform()
        context={}
        context['changepasswordform']=changepasswordform
        return render(request,'change_password.html',context)
    else:
        return HttpResponseRedirect(reverse('login'))
def forgetpassword(request):
    if request.session.get('username',default=None):
        username=request.GET['name']
        if User.objects.filter(username=username):
            password=User.objects.get(username=username).password
            email=User.objects.get(username=username).email
            send_mail('找回密码','你好，%s，你的密码为:%s。不要再忘了哦'%(username,password),'18846810840m@sina.cn',[email],fail_silently=False)
            return HttpResponse("找回成功")
        else:
            return HttpResponse("没有该用户")
    else:
        return redirect('login')













# Create your views here.
