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
    print url
    request.session['a'] = a
    return HttpResponseRedirect(url)

def callback2(request):
    oauth_verifier = request.GET['oauth_verifier']
    a = request.session.get('a', False)
    a.set_verifier(oauth_verifier)
    fi.set_auth_handler(a)
    print a
    a.save(Const.cFILENAME)
    to_json = {Const.cANUJSVIC : '200'}
    return HttpResponse(json.dumps(to_json), mimetype='application/json') 

def notify(request):
    a = request.session.get('a', False)
    
def user(request):
    #fi.set_auth_handler(Const.cFILENAME, (settings.FLICKR_API_KEY,settings.FLICKR_API_SECRET))
    fi.set_auth_handler(Const.cFILENAME)
    user = fi.test.login()
    print user
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
        
#             
# def handle_uploaded_file(filename):
#     # instead of "filename" specify the full path and filename of your choice here
#     fd = open('/Users/anujacharya/Documents/workspace/YahooHack/flickr/media/'+filename, 'w')
#     fd.write(filename['content'])
#     fd.close()

@csrf_exempt                
def photos(request):
    try:
        fi.set_auth_handler(Const.cFILENAME)
        user = fi.test.login()
        print user
        photo = request.FILES.get('image')
        photoName = photo.name
        handle_uploaded_file(photo,photoName)
        tags = request.POST.get(Const.cTAGS)
        tag = tags.split('%2C')
        tagWithSpaces = ''
        for i in tag:
            tagWithSpaces+=i+' '
        print 'tagWithSpaces'
        print tagWithSpaces
    
        # tags = 'sid anuj hack'
            
        response = fi.upload(photo_file = Const.cMEDIA+photoName, title = photoName, tags=tagWithSpaces)
        
       
        print 'after split'
        print tag
        for t in tag:
            photo = Photo.objects.create_photo(user.username,Const.cMEDIA+photoName,t)
        # Store in DB with Hash Tags
        
        to_json = {Const.cSTATUS : '203'}
    
        return HttpResponse(json.dumps(to_json), mimetype='application/json')
    except Exception as e:
        print ('Exception: %s (%s)' % (e.message, type(e)))


def image_url(imagePath):
    try:
        img = open(imagePath, "rb") 
        data = img.read() 
        print "data:image/jpg;base64,%s" % img.encode('base64') 
   
    except Exception as e:
        print ('Exception: %s (%s)' % (e.message, type(e)))
    
    
def photoSearch(request, tag=None):
    print settings.MEDIA_ROOT
    fi.set_auth_handler(Const.cFILENAME)
    user = fi.test.login()
    print 'user has given tags'
    print tag
    print 'user tag'
    
    imagesList = list()    
    result = Photo.objects.get_photo(tag,user.username)
    
    if result[Const.cRESPONSE]:
        imagesList = result[Const.cMODEL]
    
    print imagesList
    
    image_url(imagesList[0])
# 
#     to_json =  {ConstimagesList
    return HttpResponse(json.dumps('to_json'), mimetype='application/json')

def photoUpload(request):
    fi.set_auth_handler(Const.cFILENAME)
    user = fi.test.login()
    user.upload(photo_file = "path_to_the_photo_file", title = "My title")
    
# class OAuthFlickr():
#     
#     def __init__(self):
#         self.a = flickr_api.auth.AuthHandler(callback = "http://50.59.22.188:17021/flickr/callback")
#         perms = "delete"
#         self.url = self.a.get_authorization_url(perms)
 
#     def __str__(self):
#         return self.url

# def callback(request):
#     #http://50.59.22.188:17021/flickr/callback?oauth_token=72157635966888816-edb7a2b8077edea6&oauth_verifier=cb722a5cb4f7c81
#     oauth_verifier = request.GET['oauth_verifier']
#     print oauth_verifier
#     a = OAuthFlickr().getA()
#     a.set_verifier(oauth_verifier)
#     flickr_api.set_auth_handler(a)
#     a.save('token.txt')
# 
# from django.views.generic import View
# 
# class MyView(View):
#  
#     def get(self, request, *args, **kwargs):
#         f = FlickrAPI(api_key=settings.FLICKR_API_KEY,
#           api_secret=settings.FLICKR_API_SECRET,
#           callback_url='http://50.59.22.188:17021/flickr/callback')
# 
#         auth_props = f.get_authentication_tokens()
#         auth_url = auth_props['auth_url']
#         
#         #Store this token in a session or something for later use in the next step.
#         oauth_token = auth_props['oauth_token']
#         oauth_token_secret = auth_props['oauth_token_secret']
#         
#         if 'oauth_token' not in request.session:
#             request.session['oauth_token'] = oauth_token
#             request.session['oauth_token_secret'] = oauth_token_secret
# 
#         print 'Connect with Flickr via: %s' % auth_url
#         
#         return HttpResponseRedirect(auth_url)
#         
# def callback(request):
#     # oauth_token and oauth_token_secret come from the previous step
# # if needed, store those in a session variable or something
#     oauth_token = request.session.get('oauth_token', False)
#     oauth_token_secret = request.session.get('oauth_token_secret', False)
#     
#     f = FlickrAPI(api_key=settings.FLICKR_API_KEY,
#                   api_secret=settings.FLICKR_API_SECRET,
#                   oauth_token=oauth_token,
#                   oauth_token_secret=oauth_token_secret)
#     
#     
#     oauth_verifier = request.GET['oauth_verifier']
#     
#     authorized_tokens = f.get_auth_tokens(oauth_verifier)
#     
#     final_oauth_token = authorized_tokens['oauth_token']
#     final_oauth_token_secret = authorized_tokens['oauth_token_secret']
#     
#     print final_oauth_token
#     print final_oauth_token_secret
# 

    