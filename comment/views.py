from django.shortcuts import render,redirect
from .models import Question,Like_record
from django.urls import reverse
from account.models import User,Userinfo
from .form import post_question_form
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
def post_question(request,question_type):
    if request.method=="POST":
        question_type=request.session.get('question_type',default=None)
        username=request.session.get('username',default=None)
        if username:
            question_form=post_question_form(request.POST,request.FILES)
            if question_form.is_valid():
                question_text=question_form.cleaned_data['question_text']
                question_img=question_form.cleaned_data['question_img']
                user=User.objects.get(username=username)
                question=Question(user=user,question_text=question_text,question_img=question_img,question_type=question_type)
                question.save()
                referer=request.META.get('HTTP_REFERER',reverse('main'))
                return redirect(referer)
        else:
            return redirect(reverse('login'))
    else:
        request.session['question_type']=question_type
        request.session.set_expiry(0)
        question_form=post_question_form(initial={'question_text':'提问最多200字，添加图片效果更好哦'})
        context={}
        context['question_form']=question_form
        context['questions']=Question.objects.filter(question_type=question_type)
        context['question_type']=question_type
        return render(request,'question_list.html',context)
def show_main(request):
    username=request.session.get('username',default=None)
    if username:
        user=User.objects.get(username=username)
        context={}
        try:
          context['welcome_name']=Userinfo.objects.get(user=user).nickname
        except: 
          context['welcome_name']='friend'
        return render(request,'main.html',context)
    else:
        return redirect(reverse('login'))
@csrf_exempt
def show_other_user(request):
    username=request.session.get('username',default=None)
    if username:
        if request.method=="POST":
            like_status=request.POST['like_status']
            to_user_nick_name = request.session.get('other_user_name', '')
            to_user=Userinfo.objects.get(nickname=to_user_nick_name).user
            from_user = User.objects.get(username=username)
            like_record = Like_record.objects.filter(to_user=to_user, from_user=from_user)
            if like_status=="like":
                if like_record:
                    like_record[0].likes=1
                    like_record[0].save()
                else:
                    like_record=Like_record(to_user=to_user,from_user=from_user,likes=1)
                    like_record.save()
                to_user_info=to_user.userinfo.all()[0]
                to_user_info.like_num=to_user_info.like_num+1
                to_user_info.save()
                return JsonResponse({'status':'已赞'})
            else:
                if like_record:
                    like_record[0].likes = 0
                    like_record[0].save()
                else:
                    like_record = Like_record(to_user=to_user, from_user=from_user, likes=0)
                    like_record.save()
                to_user_info = to_user.userinfo.all()[0]
                to_user_info.like_num = to_user_info.like_num - 1
                to_user_info.save()
                return JsonResponse({'status': '点赞'})
        else:
            from_user=User.objects.get(username=username)
            other_user_name=request.GET.get('other_user_name','')
            request.session['other_user_name']=other_user_name
            other_user=Userinfo.objects.get(nickname=other_user_name).user
            other_user_likes_num=Userinfo.objects.get(nickname=other_user_name).like_num
            like_record=Like_record.objects.filter(to_user=other_user,from_user=from_user)
            context={}
            context['other_user_name']=other_user_name
            context['like_num']=other_user_likes_num
            if like_record:
                if like_record[0].likes==1:
                    context['like_status']="已赞"
                else:
                    context['like_status']="点赞"
            else:
                context['like_status'] = "点赞"
            return render(request,'show_other_user.html',context)
    else:
        return redirect(reverse('login'))



# Create your views here.
