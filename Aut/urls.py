from django.urls import path
from . import views


urlpatterns = [
    path('', views.auth, name='auth'),
    path('login/', views.logins, name='logins'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('change_password/', views.change_password, name='change_password'),
]
