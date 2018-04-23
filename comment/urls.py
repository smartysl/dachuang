from django.urls import path
from . import views
urlpatterns=[
    path('question/<str:question_type>/',views.post_question,name='post_question'),
    path('',views.show_main,name='main'),
    path('show-other-user',views.show_other_user,name='show_other_user'),
    path('comment',views.commment,name='comment')
]