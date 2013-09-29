from django.conf.urls import patterns, include, url
import settings
from django.conf.urls.static import  static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
# 
# from views import MyView
urlpatterns = patterns('flickr.views',
                       
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #             {'document_root': settings.STATIC_ROOT}),
#     url(r'^register$',   MyView.as_view()),
    url(r'^flickr/callback', 'callback2'),
    url(r'^index/', 'index'), # Entry point
    url(r'^user/', 'user'), # Callback form flickr
    url(r'^photo/', 'photos'), # upload photo
#     url(r'tags/', 'tag_test'),
#     url(r'notify/', 'notify'),
    url(r'^photosearch/(?P<tag>.*)$','photoSearch')
    )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
