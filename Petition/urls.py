from django.urls import path
from . import views



urlpatterns = [ 
    path('create_petition/', views.create_petition, name='create_petition'),
    path('all_petition/', views.all_petition, name='all_petition'),
    path('detail_pet/<int:id>', views.detail_pet, name='detail_pet'),
    path('create_signature/<int:p_id>', views.signature, name='create_signature'),
    path('chart/', views.chart, name='chart'),
]