from django.db                      import models
from const import Const

from django.core.exceptions         import ObjectDoesNotExist, MultipleObjectsReturned

class UserManager(models.Manager):
    def get_or_create_user(self, flickrId, username):
        error= None
        try:
            # user is the person
            # Person(id='103509102@N04', username='anujacharya1')
            user, created = self.get_or_create(flickrId=flickrId,username=username)
        except ObjectDoesNotExist:
            error = 'UserNotFound'
        except MultipleObjectsReturned:
            error = 'MultipleUserFound'
        except Exception as e:
            print ('Exception: %s (%s)' % (e.message, type(e)))
        
        if error:
            result = {Const.cRESPONSE:False, Const.cERROR:error}
        else:
            result = {Const.cRESPONSE:True, Const.cMODEL:user}
        
        return result

    def get_user(self, username):
        error= None
        try:
            user =  self.get(username=username)
        except ObjectDoesNotExist:
            error = 'UserNotFound'
        except MultipleObjectsReturned:
            error = 'MultipleUserFound'
        except Exception as e:
            print ('Exception: %s (%s)' % (e.message, type(e)))
            
        if error:
            result = {Const.cRESPONSE:False, Const.cERROR:error}
        else:
            result = {Const.cRESPONSE:True, Const.cMODEL:user}
        
        return result    
    
class User(models.Model):
    flickrId    = models.CharField(max_length=1000)
    username    = models.CharField(max_length=1000)
    
    class Meta:
        app_label       = 'flickr'
    
    def __unicode__(self):
        return u'%s' % (self.user,)
    
    objects = UserManager()
    


class PhotoManager(models.Manager):
    
    def create_photo(self, photouser, photoLoc, tag):
        error= None
        try:
            photo = self.get_or_create(user=photouser,photoLoc=photoLoc,tag=tag)
        except ObjectDoesNotExist:
            error = 'UserNotFound'
        except MultipleObjectsReturned:
            error = 'MultipleUserFound'
        except Exception as e:
            print ('Exception:PhotoManager.create_photo %s (%s)' % (e.message, type(e)))
        
        if error:
            result = {Const.cRESPONSE:False, Const.cERROR:error}
        else:
            result = {Const.cRESPONSE:True, Const.cMODEL:photo}
        
        return result

    def get_photo(self, tag, user):
        error= None
        try:
            photoLoc =  self.filter(tag=tag,user=user).values_list('photoLoc', flat=True)
        except ObjectDoesNotExist:
            error = 'UserNotFound'
        except MultipleObjectsReturned:
            error = 'MultipleUserFound'
        except Exception as e:
            print ('Exception get_photo: %s (%s)' % (e.message, type(e)))
            
        if error:
            result = {Const.cRESPONSE:False, Const.cERROR:error}
        else:
            result = {Const.cRESPONSE:True, Const.cMODEL:photoLoc}
        
        return result 
    
    
class Photo(models.Model):
    user        = models.CharField(max_length=1000)
    photoLoc    = models.CharField(max_length=1000)
    tag        = models.CharField(max_length=1000)
    
    class Meta:
        app_label       = 'flickr'
        unique_together = ("user", "photoLoc", "tag")
    
    def __unicode__(self):
        return u'%s' % (self.picLog,self.picLog)
    
    objects = PhotoManager()
    
    