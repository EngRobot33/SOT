from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.ManageUsersView.as_view(), name='manage-users'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('profile/', views.EditProfileView.as_view(), name='edit-profile'),
    path('verify-email/<uib64>/<token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('resend-email/', views.ResendEmailView.as_view(), name='resend-email'),
]
