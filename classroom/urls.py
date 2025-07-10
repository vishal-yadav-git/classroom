from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'site'

urlpatterns = [
    path("", views.index, name="home"),
    path("base/", views.base, name="base"),
    # path("register/", views.register, name="register"),
    path("lecture/", views.lecture, name="lecture"),
    path("faculty/", views.faculty, name="faculty"),
    # path("login/", views.user_login, name="login"),
    # path("logout/", views.user_logout, name="logout"),
    # path("enroll/", views.enroll, name="enroll"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    # path('product/', views.product, name='product'),
    path('lecture/<int:pk>/', views.lecture_detail, name='lecture_detail'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    # # path('newlogin/', views.newlogin, name='newlogin'),
    # # path('basic/', views.basic, name='basic'),
    # path('dashboard/', views.dashboard, name='dashboard')
]