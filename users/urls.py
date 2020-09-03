from django.urls import path
from django.contrib.auth import views as auth_views
import users.views as v

urlpatterns = [
    path('profile/become-buyer/', v.BecomeBuyer, name='become-buyer'),
    path('profile/buyer-info/', v.ManageBuyer, name='manage-buyer'),
    path('profile/delete-buyer/', v.DeleteBuyer, name='delete-buyer'),
    path('profile/vendor-info/', v.ManageVendor, name='manage-vendor'),

    path('register/', v.Register, name='register'),
    path('profile/', v.ManageAccount, name='manage-account'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password/password_reset_complete.html'), name='password_reset_complete')
]