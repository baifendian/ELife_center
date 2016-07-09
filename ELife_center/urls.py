from django.conf.urls import patterns, include, url
from django.contrib import admin
import user_manage
from ELife_center import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ELive.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    #url(r'^css/(?Ppath.*)$', 'django.views.static.serve', {'document_root': 'D:\\workspace-web\\download\\template\\css'}),
    url(r'^staticfiles/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS, 'show_indexes': True}),
    
    url(r'^user_manage/',include('user_manage.urls',namespace="user_manage"))
    
)
