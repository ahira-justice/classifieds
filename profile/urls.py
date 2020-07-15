from django.urls import path
from profile import views


app_name = 'profile'


urlpatterns = [
    path('me/', views.ProfileDetail.as_view(), name='me'),
]
