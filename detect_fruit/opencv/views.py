from django.shortcuts import render
import math
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
# Create your views here.
from django.http import HttpResponse , JsonResponse
from datetime import datetime
from django.conf import settings
# from django.http import JsonResponse

from .helper.producer_consumer_kafka import KafkaConsProd
from .helper.init import InitDetect
from .helper.db import DataBase

kf = KafkaConsProd()
dt = InitDetect()
db = DataBase()

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        # kf = KafkaConsProd()
        print('>>>>>>')
        user_id = request.COOKIES.get('user_id')
        print('user_id', user_id)
        now = datetime.now()
        myfile = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        current_name = str(math.floor(datetime.now().timestamp()))
        filename = fs.save( current_name + '_'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print ('uploaded_file_url', uploaded_file_url)
        # dt.start("/Users/niravkapoor/Documents/nirav_kapoor/personal/opencv/color-recognition/detect_fruit/opencv/img/1593118821_muskmelon.jpg", "1593118821_muskmelon.jpg", settings.MEDIA_ROOT + "/color_img")
        
        # kf.publish_message("image_url", "img", uploaded_file_url)
        # kf.check_consumer()
        count = db.insert('nsert into uploads (url, user_id, is_verified) values({uploaded_file_url},{user_id},{0})')
        print('count', count)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, "upload.html")

def upload_file(request):
    if request.method == 'POST':
        print (request.FILES)
        user_id = request.COOKIES.get('user_id')
        print('user_id', user_id)
        now = datetime.now()
        myfile = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        current_name = str(math.floor(datetime.now().timestamp()))
        filename = fs.save( current_name + '_'+ myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print ('uploaded_file_url', uploaded_file_url)
        # dt.start("/Users/niravkapoor/Documents/nirav_kapoor/personal/opencv/color-recognition/detect_fruit/opencv/img/1593118821_muskmelon.jpg", "1593118821_muskmelon.jpg", settings.MEDIA_ROOT + "/color_img")
        
        # kf.publish_message("image_url", "img", uploaded_file_url)
        # kf.check_consumer()
        count = db.insert(f'insert into uploads (url, user_id, is_verified) values({uploaded_file_url},{user_id},{0})')
        print('count', count)
        return JsonResponse({ "data": { "url" : uploaded_file_url } })
    return HttpResponse("Hello, world. You're at the polls index.")

# @api_view(['GET'])
def getDetails(request, phone):
    result = db.find("select user_id from users where phone="+phone)
    print("result", result)
    response = JsonResponse({ "data": { "user_id" : result } })
    response.set_cookie('user_id',result)
    return response

def getUploads(request, user_id):
    result = db.findAll("select * from uploads where user_id="+user_id)
    print("result", result)
    return JsonResponse({ "data": result })