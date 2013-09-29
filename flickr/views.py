'''
Created on Sep 27, 2013

@author: anujacharya
'''
# from flickrv2 import FlickrAPI

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from functools                         import wraps
from const import Const


from flickr_api.api import flickr
from xml.dom import minidom

import flickr_api as fi
try: import simplejson as json
except ImportError: import json

from django.views.decorators.csrf      import csrf_exempt

from models import Photo,User
 
def index(request):
    fi.set_keys(api_key = settings.FLICKR_API_KEY, api_secret = settings.FLICKR_API_SECRET)
    a = fi.auth.AuthHandler(callback=Const.cPORT_TUNNEL+'flickr/callback')
    perms = "delete"
    url = a.get_authorization_url(perms)
    request.session['a'] = a
    return HttpResponseRedirect(url)

def callback2(request):
    oauth_verifier = request.GET['oauth_verifier']
    a = request.session.get('a', False)
    a.set_verifier(oauth_verifier)
    fi.set_auth_handler(a)
    a.save(Const.cFILENAME)
    to_json = {Const.cANUJSVIC : '200'}
    return HttpResponse(json.dumps(to_json), mimetype='application/json')
    
def user(request):
    
    fi.set_auth_handler(Const.cFILENAME)
    user = fi.test.login()
    result = User.objects.get_or_create_user(user.id, user.username)
    user_obj_db = result[Const.cMODEL]
    to_json = {Const.cSTATUS : '200',
               Const.cUSERNAME : user_obj_db.username}
    return HttpResponse(json.dumps(to_json), mimetype='application/json')  

def handle_uploaded_file(f,fname):
    try:
        with open(Const.cMEDIA+fname, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    except Exception as e:
        print ('Exception: %s (%s)' % (e.message, type(e)))


@csrf_exempt                
def photos(request):
    try:
        fi.set_auth_handler(Const.cFILENAME)
        user = fi.test.login()
        photo = request.FILES.get('image')
        photoName = photo.name
        handle_uploaded_file(photo,photoName)
        tags = request.POST.get(Const.cTAGS)
        tag = tags.split('%2C')
        tagWithSpaces = ''
        for i in tag:
            tagWithSpaces+=i+' '
                        
        response = fi.upload(photo_file = Const.cMEDIA+photoName, title = photoName, tags=tagWithSpaces)

        for t in tag:
            photo = Photo.objects.create_photo(user.username,Const.cMEDIA+photoName,t)
        
        to_json = {Const.cSTATUS : '203'}
    
        return HttpResponse(json.dumps(to_json), mimetype='application/json')
    except Exception as e:
        print ('Exception: %s (%s)' % (e.message, type(e)))


def image_url(imagePath):
    try:
        img = open(imagePath, "rb") 
        data = img.read()
   
    except Exception as e:
        print ('Exception: %s (%s)' % (e.message, type(e)))
    
    
def photoSearch(request, tag=None):
    
    fi.set_auth_handler(Const.cFILENAME)
    user = fi.test.login()    
    imagesList = list()    
    result = Photo.objects.get_photo(tag,user.username)
    
    if result[Const.cRESPONSE]:
        imagesList = result[Const.cMODEL]
    
    mainImageList = list()
    for i in imagesList:
        iTemp  =i.split('/')
        iTempLen = len(iTemp)
        
        mainImageList.append(iTemp[iTempLen-1])
  
    to_json = {Const.cPHOTO : str(mainImageList) }

    return HttpResponse(json.dumps(to_json), mimetype='application/json')

def photoUpload(request):
    fi.set_auth_handler(Const.cFILENAME)
    user = fi.test.login()
    user.upload(photo_file = "path_to_the_photo_file", title = "My title") 

    