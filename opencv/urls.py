from django.urls import path 
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file, name='upload'),
    path('details/<phone>', views.getDetails, name='details'),
    path('get_uploads/<user_id>', views.getUploads, name='uploads'),
    path('verify_uploads/<id>', views.verifyUploads, name='uploads'),
    path('run_job', views.runJob, name='uploads')
]