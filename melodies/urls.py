from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('create/', views.create_melody, name='create_melody'),
    path('melody/<int:pk>/', views.melody_detail, name='melody_detail'),
    path('melody/<int:pk>/purchase/', views.purchase_melody, name='purchase_melody'),
    path('play-codes/', views.play_codes, name='play_codes'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
