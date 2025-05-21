from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'travel'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='travel/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('requests/', views.travel_request_list, name='travel_request_list'),
    path('requests/new/', views.travel_request_create, name='travel_request_create'),
    path('requests/success/', views.submission_success, name='submission_success'),
    path('requests/<int:pk>/edit/', views.travel_request_update, name='travel_request_update'),
    path('travel/request/', views.travel_request_create, name='travel_request_create'),

    # path('requests/', views.travel_request_list, name='travel_request_list'),
    # path('requests/new/', views.travel_request_create, name='travel_request_create'),
    path('requests/<int:pk>/', views.travel_request_detail, name='travel_request_detail'),
    path('requests/<int:pk>/update/', views.travel_request_update, name='travel_request_update'),
    path('requests/<int:pk>/delete/', views.travel_request_delete, name='travel_request_delete'),
    # path('requests/success/', views.submission_success, name='submission_success'),
]