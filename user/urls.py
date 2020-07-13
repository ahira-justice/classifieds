from django.urls import path
from user import views


app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUser.as_view(), name='create'),
    path('me/', views.UserDetail.as_view(), name='me'),
    path('token/', views.CreateToken.as_view(), name='token'),
]
