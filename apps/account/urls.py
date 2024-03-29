from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('register_phone/', views.RegistrationPhoneView.as_view()),
    path('listing/', views.UserListView.as_view()),
    path('activate/', views.ActivationView.as_view()),
    path('activation_phone/', views.ActivationPhoneView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view())
]

