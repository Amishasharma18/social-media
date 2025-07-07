from django.urls import path
from .views import dashboard_home
from . import views 
from django.contrib.auth.views import LoginView, LogoutView
from .views import twitter_login, twitter_callback



urlpatterns = [
   
    path('dashboard/', dashboard_home, name='dashboard_home'),
    path('register/', views.register_user, name='register'),
    path('login/', LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('twitter/login/', twitter_login, name='twitter_login'),
    path('twitter/callback/', twitter_callback, name='twitter_callback'),
    
]
