from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data_input/', views.data_input, name='data_input'),
    path('trace_input/', views.trace_input, name='trace_input'),
    path('trace_list/', views.trace_list, name='trace_list'),
    path('api_01/', views.api_01, name='api_01'),
    path('api_02/', views.api_02, name='api_02'),
    path('qr_code/', views.qr_code, name='qr_code'),
    path('qr_code2/', views.qr_code2, name='qr_code2'),
]
