from django import forms
from django.core.validators import RegexValidator
from account.models import User
from ckeditor.widgets import CKEditorWidget
class post_question_form(forms.Form):
    question_text=forms.CharField(label="我要提问",widget=CKEditorWidget(),max_length=200)
    question_img=forms.ImageField(label="上传问题图片",required=False)
class comment_form(forms.Form):
    comment_text=forms.CharField(label="回复",widget=CKEditorWidget(),max_length=200,error_messages={'required':'不能为空'})
    # comment_id=forms.IntegerField(widget=forms.HiddenInput())
    # comment_img=forms.ImageField(label="图片",required=False)
