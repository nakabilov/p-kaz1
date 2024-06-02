from django.urls import path
from . import views



urlpatterns = [ 
    path('table_petit/', views.table_petit, name='table_petit'),
    path('detail_petit/<int:id>/', views.detail_petit, name='detail_petit'),
    path('people_list/<int:id>/', views.people_list, name='people_list'),
    path('petition_answer/<int:id>/', views.petition_answer, name='petition_answer'),

]