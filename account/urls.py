from django.urls import path
from . import views
urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name='logout'),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('forgetpassword/',views.forgetpassword,name="forgetpassword"),
    path('edituserinfo/',views.edituserinfo,name="edituserinfo"),
    path('showuserinfo/',views.showuserinfo,name="showuserinfo"),
    path('msg/',views.msg,name="msg"),
]
