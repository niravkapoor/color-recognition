import json
import math

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse , JsonResponse
from datetime import datetime
from django.conf import settings

from .helper.producer_consumer_kafka import KafkaConsProd
from .helper.db import DataBase
from .helper.util import Util

kf = KafkaConsProd()
db = DataBase()
util = Util()

def index(request):
    return render(request, "upload.html")

def upload_file(request):
    if request.method == 'POST':
        print (request.FILES, request.method)
        user_id = request.COOKIES.get('user_id')
        print('user_id', user_id)
        now = datetime.now()
        myfile = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        current_name = str(math.floor(datetime.now().timestamp()))

        extension = myfile.name.split('.')[1].lower()
        filename = fs.save( current_name + '.'+ extension, myfile)

        data = db.insert("insert into uploads (url, user_id, is_verified, ext) values('{url}',{user_id}, false, '{extension}') RETURNING id".format(url = settings.RELATIVE_MEDIA_PATH + current_name + '.' + extension, user_id = user_id, extension = extension))

        kafkaData = { "url" : current_name + '.' + extension, "id" : data}
        print(kafkaData, data)
        kf.publish_message("image_url", "img", json.dumps(kafkaData, separators=(',', ':')))

        return JsonResponse({ "data": { "url" : settings.RELATIVE_MEDIA_PATH + current_name + '.' + extension, "user_id": user_id, "is_verified": 0, "id": data}})
    return util.constructResponse(404)

def getDetails(request, phone):
    result = db.find("select user_id from users where phone="+phone)
    response = JsonResponse({ "data": { "user_id" : result } })
    response.set_cookie('user_id',result)
    return response

def getUploads(request, user_id):
    result = db.findAll("select * from uploads where user_id="+user_id)
    response = JsonResponse({ "data": result })
    response.set_cookie('user_id',user_id)
    return response

def verifyUploads(request, id):
    if request.method == 'PUT':
        result = db.update("update uploads set is_verified = true where id = {id} RETURNING *".format(id = id))
        return JsonResponse({ "data": "true" })

    return util.constructResponse(404)

def runJob(request):
    kf.check_consumer()
    return HttpResponse("Kafka executed successfully")