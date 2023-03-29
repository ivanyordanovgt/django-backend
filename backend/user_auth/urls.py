from django.urls import re_path, include

from django.contrib import admin
from django.urls import path
import user_auth.views as views

urlpatterns = [
    path('register', views.registerView.as_view()),
    path('login', views.loginView.as_view()),
    path('user', views.UserView.as_view()),
    path('logout', views.LogoutView.as_view())

]
