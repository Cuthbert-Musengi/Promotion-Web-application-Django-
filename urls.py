

''' Cuthbert Musengi +263778241753'''
"""promotionSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from promotion.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',index,name='index'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),

    path('singup', signup, name='signup'),
    path('profile', profile, name='profile'),
    path('upload_cv', upload_cv, name='upload_cv'),
    path('view_mycv', view_mycv, name='view_mycv'),

    path('login', userlogin, name='login'),
    path('admin_login', admin_login, name='admin_login'),
    path('admin_home', admin_home, name='admin_home'),
    path('view_users', view_users, name='view_users'),
    path('pending_resume', pending_resume, name='pending_resume'),
    path('promoted_cv', promoted_cv, name='promoted_cv'),
    path('assign_promotion/<int:pid>', assign_promotion, name='assign_promotion'),
    path('all_cv', all_cv, name='all_cv'),
    path('rejected_cv', rejected_cv, name='rejected_cv'),
    path('delete_mycv/<int:pid>', delete_mycv, name='delete_mycv'),
    path('delete_cv/<int:pid>', delete_cv, name='delete_cv'),
    path('delete_users/<int:pid>', delete_users, name='delete_users'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('changepassword', changepassword, name='changepassword'),
    path('logout', Logout, name='logout'),
    path('change_passwordadmin', change_passwordadmin, name='change_passwordadmin'),
    path('unread_queries', unread_queries, name='unread_queries'),
    path('read_queries', read_queries, name='read_queries'),
    path('view_queries/<int:pid>', view_queries, name='view_queries'),
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


