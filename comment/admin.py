from django.contrib import admin
from .models import Question,Like_record,Comment,History_record
admin.site.register(Question)
admin.site.register(Like_record)
admin.site.register(Comment)
admin.site.register(History_record)
# Register your models here.
