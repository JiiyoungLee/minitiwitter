from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login, name='login'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^main/(?P<user_id>\d+)/$', views.timeline, name='timeline'),
	url(r'^main/(?P<user_id>\d+)/me/$', views.mytimeline, name='mytimeline'),
	url(r'^login/help/$', views.helpauth, name='helpauth'),
	url(r'^findid/$', views.helpfindid, name='helpfindid'),
	url(r'^findpw$', views.helpfindpw, name='helpfindpw'),
	url(r'^article/(?P<user_id>\d+)/write/$', views.writearticle, name='article'),
	url(r'^article/(?P<article_id>\d+)/modify/$', views.modifyarticle, name='article'),
	url(r'^user/(?P<user_id>\d+)/$', views.userInfo, name='userInfo'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^uploads/(?P<file>.+)', views.uploads, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)