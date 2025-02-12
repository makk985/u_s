from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile_view, name='profile'),
    path('service', views.service_request_view, name='service_request'),
    path('track', views.track_request_view, name='track_request'),
    path('staff/dashboard', views.staff_dashboard, name='staff_dashboard'),
    path('staff/service/<int:pk>/update', views.service_update_view, name='service_update'),
    path('staff/service_docs/<int:pk>/', views.service_docs, name='service_docs'),
]