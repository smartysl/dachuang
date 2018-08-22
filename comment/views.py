from django.shortcuts import render,redirect
from .models import Question,Like_record,Comment,History_record,Admire_record,Initial_integral
from django.urls import reverse
from account.models import User,Userinfo
from .form import post_question_form,comment_form
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from comment.models import History_record
from comment.models import Comment

from itertools import chain
@csrf_exempt
def post_question(request,question_type):
    username=request.session.get('username',default=None)
    user=User.objects.get(username=username)
    context0={}
    try:
        context0['your_headimg']=Userinfo.objects.get(user=user).headimg.url
    except:
        context0['your_headimg']=''
    if request.method=="POST":
        # question_type=request.session.get('question_type',default=None)
        username=request.session.get('username',default=None)
        if username:
            question_type=request.POST['question_type']
            reward_integral=int(request.POST['reward_integral'])
            question_form=post_question_form(request.POST,request.FILES)
            if question_form.is_valid():
                question_text=question_form.cleaned_data['question_text']
                question_img=question_form.cleaned_data['question_img']
                question=Question(user=user,question_text=question_text,question_img=question_img,question_type=question_type,reward_integral=reward_integral)
                user.integral-=reward_integral
                question.save()
                user.save()
                referer=request.META.get('HTTP_REFERER',reverse('main'))
                return redirect(referer)
        else:
            return redirect(reverse('login'))
    else:
        request.session['question_type']=question_type
        request.session.set_expiry(0)
        question_form=post_question_form(initial={'question_text':'提问最多200字，添加图片效果更好哦'})
        all_questions=Question.objects.filter(question_type=question_type)
        paginator=Paginator(all_questions,6)
        page_num=int(request.GET.get('page',1))
        questions_of_page=paginator.get_page(page_num)
        current_page=questions_of_page.number
        page_range=list(range(max(current_page-2,1),current_page))+list(range(current_page,min(current_page+2,paginator.num_pages)+1))
        context={}
        context['first_shown_page_num']=page_range[0]
        context['last_shown_page_num']=page_range[-1]
        context['page_range']=page_range
        context['question_form']=question_form
        context['questions_of_page']=questions_of_page
        context['question_type']=question_type
        context['max_integral']=user.integral
        context.update(context0)
        return render(request,'question_list.html',context)
@csrf_exempt
def show_main(request):
    username=request.session.get('username',default=None)
    if username:
        user=User.objects.get(username=username)
        integral_record,is_created=Initial_integral.objects.get_or_create(user=user)
        context={}
        marjors = ['jisuanji','jingjiguanli','xinli','waiyu','history','gongxue','lixue','shengming','zhexue','faxue','edu']

        for marjor in marjors:
            context[marjor]=Question.objects.filter(question_type=marjor)[:5]
        if request.method == 'POST':
            if not integral_record.is_aquired:
                if request.POST.get('get_integral'):
                    integral_record.is_aquired=1
                    user.integral+=100
                    integral_record.save()
                    user.save()
                    return JsonResponse({})
        else:
            userinfo=Userinfo.objects.filter(user=user)
            user_comment_msgs,user_admire_msgs=Comment.objects.filter(reply_user=user,is_read=0),Admire_record.objects.filter(admire_user=user,is_read=0)
            user_msgs=chain(user_comment_msgs,user_admire_msgs)
            count=0;
            if userinfo:
                for user_msg in user_msgs:
                    if user_msg.is_read==0:
                        count+=1
            context['msg_num']=count
            if integral_record.is_aquired:
                context['is_aquired']='1'
            try:
                context['welcome_name']=Userinfo.objects.get(user=user).nickname
                context['your_headimg']=Userinfo.objects.get(user=user).headimg.url
            except:
                context['welcome_name']='friend'
                context['your_headimg']=''
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
            other_userinfo=Userinfo.objects.filter(user=other_user)
            like_record=Like_record.objects.filter(to_user=other_user,from_user=from_user)
            context={}
            context['other_userinfo']=other_userinfo[0]
            context['like_num']=other_user_likes_num
            context['integral']=other_user.integral
            try:
                context['your_headimg']=Userinfo.objects.get(user=from_user).headimg.url
            except:
                context['your_headimg']=''
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
        user = User.objects.get(username=username)
        if request.method=="POST":
            if request.POST.get('comment_type'):
                text_form=comment_form(request.POST)
                comment=Comment()
                if text_form.is_valid():
                    comment.comment_text = text_form.cleaned_data['comment_text']
                parent_comment_id=request.POST['comment_id']
                comment.comment_type=request.POST['comment_type']
                comment.comment_img=request.FILES.get('comment_img')
                comment.comment_user=user
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
                    user.integral+=3
                comment.save()
                user.save()
                data={'comment_text':comment.comment_text,'comment_date':comment.comment_time,'comment_id':comment.pk}
                try:
                    data['nickname']=comment.comment_user.userinfo.all()[0].nickname
                except:
                    data['nickname']=comment.comment_user.username
                return JsonResponse(data)
            else:
                comment_id=request.POST['comment_id']
                question_id=request.POST['question']
                comment = Comment.objects.get(pk=comment_id)
                question=Question.objects.get(pk=question_id)
                if question.user==user:
                    admire_status=request.POST['admire']
                    admire_record = Admire_record()
                    admire_record.admire_comment = comment
                    admire_record.question=question
                    admire_record.user=user
                    admire_record.admire_user=comment.comment_user
                    if admire_status == "yes":
                        admire_record.is_admired=1
                        user.integral+=question.reward_integral//3+5
                        data={'admire_status':'is_admired'}
                    else:
                        admire_record.is_admired=0
                        data={'admire_status':'not_admired'}
                    user.save()
                    admire_record.save()
                    return JsonResponse(data)
        else:
            user=User.objects.get(username=username)
            question_id=request.GET.get("question_id")
            question=Question.objects.get(pk=question_id)
            comments=Comment.objects.filter(comment_question=question,parent_comment=None)
            all_comments=Comment.objects.filter(comment_question=question)
            history_record=History_record()
            history_record.user=User.objects.get(username=username)
            history_record.viewed_question=question
            history_record.save()
            admire_record=Admire_record.objects.filter(user=user,question=question)
            context={}
            context['all_comments']=all_comments
            context['admire_records']=admire_record
            context['comments']=comments.order_by('comment_time')
            context['question']=question
            context['comment_form']=comment_form()
            if question.user==user:
                context['is_user']='1'
            try:
                context['your_headimg']=Userinfo.objects.get(user=user).headimg.url
            except:
                context['your_headimg']=''
            return render(request,'question_detail.html',context)
def delete(request):
    username=request.session.get('username',default=None)
    user=User.objects.get(username=username)
    if request.GET['able_to_del']:
        id=int(request.GET['id'])
        if Comment.objects.get(pk=id).comment_user == user:
            return JsonResponse({'able_to_del':'1'})
        else:
            return JsonResponse({'able_to_del':'0'})
    if request.GET['key'] == 'comment':
        del_id=int(request.GET['value'])
        del_comment=Comment.objects.get(pk=del_id)
        del del_id
    else:
        del_id = int(request.GET['value'])
        del_question=Question.objects.get(pk=del_id)
        del del_id
    return JsonResponse({'status': 'success'})

# Create your views here.
