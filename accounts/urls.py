from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # path('login/', views.login_view, name='login'),
    path('login/', views.loginOrg, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('render_404', views.render_404, name='render_404'),
    # path('password_change/', change_password, name='password_change'),
    
    
    # Pasword Reset Patterns and Views
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
         name="reset_password"),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
         name="password_reset_complete"),
   
]
