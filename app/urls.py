from django.urls import path, include


urlpatterns = [
    path('api/user/', include('user.urls')),
]
