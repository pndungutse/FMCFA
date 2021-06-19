from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # path('login/', views.login_view, name='login'),
    path('login/', views.loginOrg, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('render_404', views.render_404, name='render_404'),
    # path('password_change/', change_password, name='password_change'),
   
]
