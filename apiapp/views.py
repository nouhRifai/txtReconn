from django.shortcuts import render
from rest_framework import viewsets
from .models import awsimage
from .serializers import awsimageSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import base64
import secrets
import cv2
import pytesseract

class awsimageView(viewsets.ModelViewSet):
    queryset = awsimage.objects.all()
    serializer_class = awsimageSerializer
    

    #redefine create function
    def create(self, request, *args, **kwargs):
        #extract the image (base64) and the title
        image = request.data['image']
        title = request.data['title']
        #make a new name for the image to avoid conflict
        filename = secrets.token_hex(nbytes=16)
        #attach filename to a relative path
        filepath = "media/"+filename+".png"
        #open the file, that we just created its name with write binary moide
        im = open(filepath,"wb")
        #decode the base64 string acquired from the request
        im.write(base64.b64decode(image))
        #close the file
        im.close()
        img = cv2.imread(filepath)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_string(img)
        print(result[0:15])
        #store in the database
        # awsimage.objects.create(title = title, image = myImage)
        return JsonResponse({'message': 'image created', 'content':result}, status=200)


