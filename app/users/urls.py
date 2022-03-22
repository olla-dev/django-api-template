from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.CreateUserView.as_view(), name="create"),
    path('auth', views.CreateAuthTokenView.as_view(), name="auth"),
    path('me', views.ManagerUserView.as_view(), name="me")
]