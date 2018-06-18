from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from .models import User,Userinfo
from comment.models import Admire_record
from .form import Userregisterform,Userloginform,Changepasswordform,Userinfoform
from django.urls import reverse
from django.core.mail import send_mail
from comment.models import History_record
from comment.models import Comment
from itertools import chain
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
                    User.objects.create(username=username,password=bathhash(password),email=email)
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
            user=User.objects.filter(username=username)
            if user:
                if user[0].password==bathhash(password):
                    request.session['username']=username
                    request.session.set_expiry(0)
                    return redirect(reverse('main'))
                else:
                    loginform.add_error(None,"用户名或密码错误")
            else:
                loginform.add_error(None, "用户名或密码错误")
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
        return redirect(reverse('login'))
def edituserinfo(request):
    if request.session.get('username',default=None):
        username = request.session['username']
        user = User.objects.get(username=username)
        if user.userinfo.all():
            userinfo=Userinfo.objects.get(user=user)
            if request.method=="POST":
                userinfoform = Userinfoform(request.POST, request.FILES)
                if userinfoform.is_valid():
                    userinfo.headimg = userinfoform.cleaned_data['headimg']
                    userinfo.nickname = userinfoform.cleaned_data['nickname']
                    userinfo.tel = userinfoform.cleaned_data['tel']
                    userinfo.QQ = userinfoform.cleaned_data['QQ']
                    userinfo.school = userinfoform.cleaned_data['school']
                    userinfo.major = userinfoform.cleaned_data['major']
                    userinfo.grade = userinfoform.cleaned_data['grade']
                    userinfo.aboutme = userinfoform.cleaned_data['aboutme']
                    userinfo.save()
                    return redirect(reverse('showuserinfo'))
                else:
                    return HttpResponse('修改失败')

            else:
                data={'email':user.email,'nickname':userinfo.nickname,'tel':userinfo.tel,'QQ':userinfo.QQ,'school':userinfo.school
                                                   ,'major':userinfo.major,'grade':userinfo.grade,'aboutme':userinfo.aboutme}
                if not userinfo.aboutme:
                    data['aboutme']='这个人很懒，什么也没有留下'
                userinfoform=Userinfoform(initial=data)
                context={}
                context['userinfo_form']=userinfoform
                return render(request,'edituserinfo.html',context)
        else:
            if request.method=="POST":
                userinfoform = Userinfoform(request.POST, request.FILES)
                if userinfoform.is_valid():
                    headimg = userinfoform.cleaned_data['headimg']
                    nickname = userinfoform.cleaned_data['nickname']
                    tel = userinfoform.cleaned_data['tel']
                    QQ = userinfoform.cleaned_data['QQ']
                    school = userinfoform.cleaned_data['school']
                    major = userinfoform.cleaned_data['major']
                    grade = userinfoform.cleaned_data['grade']
                    aboutme = userinfoform.cleaned_data['aboutme']
                    Userinfo.objects.create(user=user, nickname=nickname, headimg=headimg, tel=tel, QQ=QQ, school=school,
                                        major=major, grade=grade, aboutme=aboutme)
                    return redirect(reverse('showuserinfo'))
            else:
                userinfoform = Userinfoform(initial={'email': user.email,'aboutme': '这个人很懒，什么也没有留下'})
                context = {}
                context['userinfo_form'] = userinfoform
                return render(request, 'edituserinfo.html', context)
    else:
        return redirect(reverse('login'))
def showuserinfo(request):
    if request.session.get('username',default=None):
        context={}
        username=request.session['username']
        user=User.objects.get(username=username)
        userinfo=Userinfo.objects.filter(user=user)
        if userinfo:
            context['history_records']=History_record.objects.filter(user=user)[:30]
            context['userinfo']=userinfo[0]
        else:
            context['error_msg']='该用户尚未填写个人信息'
        return render(request,'show_user_info.html',context)
    else:
        return redirect(reverse('login'))
def bathhash(list):
    fold_num=0
    asi_list=''
    i=0
    for j in list:
        asi_list+=str(ord(j))
    while(i<len(asi_list)-1):
        fold_num+=int(asi_list[i]+asi_list[i+1])
        i+=2
    if(len(asi_list)%2==1):
        fold_num+=int(asi_list[-1])
    hash=str(fold_num*fold_num)[:2]+str(fold_num*fold_num)[-2:]
    return hash
def msg(request):
    count=0
    username=request.session.get('username',default=None)
    if username:
         user=User.objects.get(username=username)
         context={}
         userinfo=Userinfo.objects.filter(user=user)
         user_comment_msgs,user_admire_msgs=Comment.objects.filter(reply_user=user,is_read=0),Admire_record.objects.filter(admire_user=user,is_read=0)
         user_msgs=chain(user_comment_msgs,user_admire_msgs)
         readed_comment_msgs,readed_admire_msgs=Comment.objects.filter(reply_user=user,is_read=1),Admire_record.objects.filter(admire_user=user,is_read=1)
         readed_msgs=chain(readed_comment_msgs,readed_admire_msgs)
         if userinfo:
             context['user_comment_msgs'],context['user_admire_msgs'],context['readed_comment_msgs'],context['readed_admire_msgs']=user_comment_msgs.order_by('-comment_time'),user_admire_msgs.order_by('-admire_time'),readed_comment_msgs.order_by('-comment_time'),readed_admire_msgs.order_by('-admire_time')
             for user_msg in user_msgs:
                 user_msg.is_read=1
                 user_msg.save()
                 count+=1
             context['msg_num']=count
             if count == 0:
                 context['no_msg']='亲，没有新的消息哦~'
         else:
             context['error_msg']='请填写个人资料'
         return render(request,'msg.html',context)
    else:
         return redirect(reverse('login'))
# Create your views here.
