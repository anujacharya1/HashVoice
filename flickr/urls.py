from django.conf.urls import patterns, include, url
import settings
from django.conf.urls.static import  static

# from views import MyView
urlpatterns = patterns('flickr.views',

    url(r'^flickr/callback', 'callback2'),
    url(r'^index/', 'index'), # Entry point
    url(r'^user/', 'user'), # Callback form flickr
    url(r'^photo/', 'photos'), # upload photo
    url(r'^photosearch/(?P<tag>.*)$','photoSearch')
    )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
