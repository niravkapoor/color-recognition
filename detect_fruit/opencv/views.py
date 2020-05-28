from django.shortcuts import render
import math
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings

from .helper.producer_consumer_kafka import KafkaConsProd

kf = KafkaConsProd()

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        # kf = KafkaConsProd()
        now = datetime.now()
        myfile = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        current_name = str(math.floor(datetime.now().timestamp()))
        filename = fs.save( current_name + '_'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print ('uploaded_file_url', uploaded_file_url)
        kf.publish_message("image_url", "img", uploaded_file_url)
        kf.check_consumer()
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, "upload.html")

def upload_file(request):
    if request.method == 'POST':
        print (request.FILES)
    return HttpResponse("Hello, world. You're at the polls index.")