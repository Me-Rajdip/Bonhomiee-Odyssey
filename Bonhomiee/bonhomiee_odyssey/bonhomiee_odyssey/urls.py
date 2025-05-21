from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from travel import views as travel_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page
    path('', travel_views.home_page, name='home'),
    
    # Include travel app URLs without prefix
    path('', include('travel.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    
    # path('accounts/logout/', auth_views.LogoutView.as_view(
    #     template_name='travel/logged_out.html',
    #     next_page='home'
    # ), name='logout'),
    
    # # Authentication URLs
    # path('accounts/login/', auth_views.LoginView.as_view(
    #     template_name='travel/login.html',
    #     redirect_authenticated_user=True
    # ), name='login'),

    path('login/', auth_views.LoginView.as_view(template_name='travel/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='travel/logout.html'), name='logout'),
    path('register/', auth_views.LogoutView.as_view(template_name='travel/register.html'), name='register'),
    
]