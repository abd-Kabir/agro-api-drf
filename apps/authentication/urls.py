from django.urls import path
from apps.authentication.views import LogoutView, RegisterUser, ObtainAuthTokeAPI

app_name = 'auth'
urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    path('login/', ObtainAuthTokeAPI.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]
