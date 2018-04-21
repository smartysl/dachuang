from django import forms
from django.core.validators import RegexValidator
from account.models import User
from ckeditor.widgets import CKEditorWidget
class post_question_form(forms.Form):
    question_text=forms.CharField(label="我要提问",widget=CKEditorWidget(),max_length=200)
    question_img=forms.ImageField(label="上传问题图片",required=False)
