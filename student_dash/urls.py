from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views
# from .views import user_login, register, user_logout

app_name = 'student_dash'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("base/", views.dash_base, name="dash_base"),
    path("lecture/", views.lecture_view, name="lecture"),
    path("playlist/", views.playlist_lecture_view, name="playlist_lecture_view"),
    path("profile", views.profile, name="profile"),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    

]