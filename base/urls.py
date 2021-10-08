from django.urls import path
from . import views 


urlpatterns = [

    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.Userlogout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('settings/', views.settings, name='settings'),
    path('updateaccounts/', views.updateaccounts, name='updateaccounts'),

]