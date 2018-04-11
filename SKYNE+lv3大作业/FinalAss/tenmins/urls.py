"""tenmins URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from website.views import listing, index_login, index_register, detail, detail_vote, index, GetAuthToken
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from website.mobile_views import video_list, user_list, user_detail, mobile_login
from website.api import video, video_card, userlist, update_user, get_user, change_user, ban_user, is_Author


urlpatterns = [
    url(r'^$', index,name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^list/$', listing, name='list'),
    url(r'^list/(?P<cate>[A-Za-z]+)$', listing, name='list'),
    url(r'^detail/(?P<id>\d+)$', detail, name='detail'),
    url(r'^detail/vote/(?P<id>\d+)$', detail_vote, name='vote'),
    url(r'^login/$', index_login, name='login'),
    url(r'^register/$', index_register, name='register'),
    url(r'^logout/$', logout, {'next_page': '/register'}, name='logout'),

    url(r'^api/videos/$', video),
    url(r'^api/videos/(?P<id>\d+)$', video_card),
    url(r'^api/token-auth$', GetAuthToken.as_view()),

    url(r'^m/videolist/$', video_list),
    # 上面的url路由皆是lession10部分，勿改勿动。
    url(r'^m/userlistpanel/$', user_list, name='user_list'),
    url(r'^m/userdetail/(?P<id>\d+)/$', user_detail, name='user_detail'),
    url(r'^m/userlistpanel/login/$', mobile_login, name='mobile_login'),

    #新增加的对应的API路由的地址
    url(r'^api/token-auth-admin$', GetAuthToken.as_view()),
    url(r'^api/userlist/$', userlist),
    url(r'^api/userdetail/$', update_user),
    url(r'^api/getusername/$', get_user),
    url(r'^api/changeuser/(?P<id>\d+)$', change_user),
    url(r'^api/banuser/(?P<id>\d+)$', ban_user),
    url(r'^api/isauthor/$', is_Author),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
