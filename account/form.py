from django import forms
from django.core.validators import RegexValidator
class Userregisterform(forms.Form):
    username=forms.CharField(max_length=10,label="用户名")
    password=forms.CharField(max_length=10,min_length=6,widget=forms.PasswordInput,label="密码",error_messages={
        'required':'密码不能为空','max_length':'最大长度不能超过十个字节','min_length':'最小长度不能小于六个字节'
    },validators=[RegexValidator('^[A-Za-z]+','密码必须由字母开头')])
    passwordagain=forms.CharField(max_length=10,widget=forms.PasswordInput,label="确认密码")
    email=forms.EmailField(label="email")
class Userloginform(forms.Form):
    username=forms.CharField(max_length=10,label="用户名")
    password=forms.CharField(max_length=10,widget=forms.PasswordInput,label="密码")
class Changepasswordform(forms.Form):
    originalpassword=forms.CharField(max_length=10,label="原密码")
    newpassword=forms.CharField(max_length=10,min_length=6,widget=forms.PasswordInput,label="新密码",error_messages={
        'required':'密码不能为空','max_length':'最大长度不能超过十个字节','min_length':'最小长度不能小于六个字节'
    },validators=[RegexValidator('^[A-Za-z]+','密码必须由字母开头')])
    newpasswordagain=forms.CharField(max_length=10,min_length=6,label="确认密码",widget=forms.PasswordInput)