from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('opencv/', include('opencv.urls')),
]

