from django.urls import path

from .views import registration, authentication, logout


urlpatterns = [
    path('signup', registration),
    path('login', authentication),
    path('logout', logout)
]
