from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('register/success/', VerifySuccessView.as_view(), name='register_success'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/confirm/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/complete/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('simple/reset/', simple_reset_password, name='simple_reset'),
    path('user_list/', UsersListView.as_view(), name='user_list'),
    path('user_change/<int:pk>/', user_status_change, name='user_change')

]