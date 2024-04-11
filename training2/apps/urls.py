from django.urls import path, include


urlpatterns = [
    path('', include('apps.entrance.urls')),
    path('', include('apps.production.urls'))
]
