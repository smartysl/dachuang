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
# Create your models here.
