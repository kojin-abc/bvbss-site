from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('logoutv', views.logoutv, name='logoutv'),
    path('select', views.select, name='select'),
    path('today', views.today, name='today'),
    path('opponent', views.opponent, name='opponent'),
    path('input_t/<int:num>/', views.input_t, name='input_t'),
    path('input_p/<int:g_num>/<int:p_num>/', views.input_p, name='input_p'),
    path('input_r/<int:num>/', views.input_r, name='input_r'),
    path('look', views.look, name='look'),
    path('look_day/<str:gstr>/', views.look_day , name='look_day'),
    path('look_summary/<gstr1>/<gstr2>/<gnumstr>/', views.look_summary, name='look_summary'),
    path('look_detail/<gstr1>/<gstr2>/<gnumstr>/', views.look_detail, name='look_detail'),
    path('look_fix/<gstr1>/<gstr2>/<gnumstr>/', views.look_fix, name='look_fix'),
]