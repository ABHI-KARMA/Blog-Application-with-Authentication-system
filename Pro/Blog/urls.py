from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('about/',about,name="about"),
    path('post/<int:pk>',post,name="post"),
    path('contact/',contact,name="contact"),
    path("login/",login_user,name='LOGIN'),
    path("register/",register,name='REGISTER'),
    path('logout/',logout_user,name='LOGOUT'),
    path("tokensend/",token_send,name='TOKENSEND'),
    path("success/",success,name='SUCCESS'),
    path("verify/<auth_token>",verify,name='VERIFY'),
    path("error/",error_page,name='ERROR'),
    path("forgot-password/",forgotPass,name='FORGOTPASS'),
    path("recreate-password/<token>/",recreatePass,name='RECREATEPASS'),
]
