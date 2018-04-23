from django.shortcuts import render,redirect
from .models import Question,Like_record,Comment
from django.urls import reverse
from account.models import User,Userinfo
from .form import post_question_form,comment_form
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def post_question(request,question_type):
    if request.method=="POST":
        # question_type=request.session.get('question_type',default=None)
        username=request.session.get('username',default=None)
        if username:
            question_type=request.POST['question_type']
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
@csrf_exempt
def commment(request):
    username=request.session.get('username',default=None)
    if username:
        if request.method=="POST":
            comment_post_form=comment_form(request.POST)
            if comment_post_form.is_valid():
                comment=Comment()
                comment.comment_text=comment_post_form.cleaned_data['comment_text']
                parent_comment_id=comment_post_form.cleaned_data['comment_id']
                comment.comment_user=User.objects.get(username=username)
                parent_comment=Comment.objects.filter(pk=parent_comment_id)
                if parent_comment:
                    comment.parent_comment=parent_comment[0]
                    comment.root_comment=parent_comment[0].root_comment if not parent_comment[0].root_comment is None else parent_comment[0]
                    comment.reply_user=parent_comment[0].comment_user
                else:
                    comment.parent_comment=None
                    comment.root_comment=None
                    question_id=request.POST['question_id']
                    comment.comment_question=Question.objects.get(pk=question_id)
                    comment.reply_user=Question.objects.get(pk=question_id).user
                comment.save()
                data={'nickname':comment.comment_user.userinfo.all()[0].nickname,'comment_text':comment.comment_text,'comment_date':comment.comment_time,'comment_id':comment.pk}
                return JsonResponse(data)
            else:
                return JsonResponse({'status':'fail'})
        else:
            question_id=request.GET.get("question_id")
            question=Question.objects.get(pk=question_id)
            comments=Comment.objects.filter(comment_question=question,parent_comment=None)
            context={}
            context['comments']=comments.order_by('-comment_time')
            context['question']=question
            context['comment_form']=comment_form(initial={'comment_id':0})
            return render(request,'question_detail.html',context)



# Create your views here.
