from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file, name='upload'),
    path('details/<phone>', views.getDetails, name='details'),
    path('get_uploads/<user_id>', views.getUploads, name='uploads'),
    
]