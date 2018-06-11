from django.db import models
class User(models.Model):
    username=models.CharField(max_length=10)
    password=models.CharField(max_length=10)
    email=models.EmailField()
    integral=models.IntegerField(default=0)
    def __str__(self):
        return self.username
class Userinfo(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="userinfo")
    nickname=models.CharField(max_length=7)
    headimg=models.ImageField(upload_to='headimg',default='headimg/苹果1_0OtvrIb.jpg')
    tel=models.CharField(max_length=20)
    QQ=models.CharField(max_length=20)
    school=models.CharField(max_length=20)
    major=models.CharField(max_length=20)
    grade=models.CharField(max_length=10)
    aboutme=models.CharField(max_length=100)
    like_num=models.IntegerField(default=0)
    def __str__(self):
        return self.tel

