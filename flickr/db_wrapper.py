## Django or 3rd party packages
from django.core.exceptions        import ObjectDoesNotExist, MultipleObjectsReturned
import logging
from functools                      import wraps
try: import simplejson as json
except ImportError: import json

from flickr.models                  import User


logger = logging.getLogger('logview.groups')

class DbWrapper:
    
    def __init__(self,requestType,requestCmd, owner):
        self.requestType    = requestType
        self.requestCmd     = requestCmd
        self.owner          = owner 

    