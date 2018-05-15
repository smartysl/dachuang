from django.db import models
from account.models import User
class Question(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    question_type=models.CharField(max_length=50)
    question_text=models.CharField(max_length=200)
    question_date=models.DateTimeField(auto_now_add=True)
    question_img=models.ImageField(upload_to='question_img',null=True)
class Like_record(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="from_user")
    to_user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="to_user")
    likes=models.IntegerField(default=0)
class Comment(models.Model):
    comment_question=models.ForeignKey(Question,on_delete=models.DO_NOTHING,null=True)
    comment_type=models.IntegerField(default=0)
    comment_user=models.ForeignKey(User,related_name="comment",on_delete=models.DO_NOTHING)
    reply_user=models.ForeignKey(User,related_name="reply",on_delete=models.DO_NOTHING)
    comment_text=models.TextField()
    comment_time=models.DateTimeField(auto_now_add=True)
    parent_comment=models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING,related_name="parent")
    root_comment=models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING,related_name="root")
    comment_img=models.ImageField(upload_to='answer_img',null=True)
    class Meta:
        ordering=['comment_time']
class History_record(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    viewed_question=models.ForeignKey(Question,on_delete=models.DO_NOTHING)
    view_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-view_time']
class Admire_record(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    admire_comment=models.ForeignKey(Comment,on_delete=models.DO_NOTHING)
    admire_time=models.DateTimeField(auto_now_add=True)
    is_admired=models.IntegerField(default=0)
# Create your models here.
