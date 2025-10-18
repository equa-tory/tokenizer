from django.urls import path, re_path, include

from . import views


urlpatterns = [
    path('redir',views.redir,name='redir'),
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('api/token/', views.token_data, name='token_data'),
    path('api/add-token', views.add_token),
]