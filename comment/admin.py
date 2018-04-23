from django.contrib import admin
from .models import Question,Like_record,Comment
admin.site.register(Question)
admin.site.register(Like_record)
admin.site.register(Comment)
# Register your models here.
