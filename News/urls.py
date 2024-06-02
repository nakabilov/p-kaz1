from django.urls import path
from . import views

# app_name = 'news'

urlpatterns = [
    path('create_news/<int:p_id>', views.create_news, name='create_news'),
    path('index/', views.index, name='index'),
    path('detail_news/<int:id>', views.detail_news, name='detail_news'),
    path('like/<int:n_id>/', views.like, name='like'),
   
]