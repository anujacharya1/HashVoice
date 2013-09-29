
import re

try: import simplejson as json
except ImportError: import json

from functools                      import wraps

flickr_uriPath = "/register"

def parseClientGetRequest(path, requestMethod):
    
    flickr_request_type = re.split(flickr_uriPath, path)
    cmd_resource = ''
  
    if len(flickr_request_type) == 2:
        # Only specific to Conference request type
        cmd_part = re.split('/', flickr_request_type[1])
        cmd_resource = cmd_part[1]
        
        if requestMethod == 'GET':
            # create/terminate conference
            action = 'register'
            if len(cmd_part) > 2:
                action = cmd_part[2]
               
       
    
