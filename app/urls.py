from django.urls import path, include


urlpatterns = [
    path('api/user/', include('user.urls')),
    path('api/profile/', include('profile.urls')),
    path('api/items/', include('item.urls')),
]
