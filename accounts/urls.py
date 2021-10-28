from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('', views.home, name='home'),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('admin-login', views.admin, name="admin-login"),
    path('admin-dash', views.admindash, name="admin-dash"),
    path('delete/<str:pk>/', views.delete, name="delete"),
    path('update/<str:pk>/', views.update, name="update"),
    path('adminlogout', views.adminlogout, name="adminlogout"),
    path('block-user/<str:pk>/',views.blockuser, name='block-user'),
    path('unblock-user/<str:pk>/',views.unblockuser, name='unblock-user'),
    path('adduser', views.adduser, name="adduser"),
    
]