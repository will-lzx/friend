"""friendplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from weixin import views

urlpatterns = [
    url(r'^wx/$', views.wx, name='wx'),
    url(r'^privatecenter/$', views.privatecenter, name='privatecenter'),
    url(r'^latest/$', views.latest, name='latest'),
    url(r'^history/$', views.history, name='history'),
    url(r'^beauty/$', views.beauty, name='beauty'),
    url(r'^expert/$', views.expert, name='expert'),

    url(r'^coordinate/$', views.coordinate, name='coordinate'),
    url(r'^member_join/$', views.member_join, name='member_join'),
    url(r'^show_member/$', views.show_member, name='show_member'),

    url(r'^update_member/$', views.update_member, name='update_member'),

    url(r'^expert_join/$', views.expert_join, name='expert_join'),
    url(r'^show_expert/$', views.show_expert, name='show_expert'),

    url(r'^save_member/$', views.save_member, name='save_member'),
    url(r'^detail_submit/$', views.detail_submit, name='detail_submit'),
    url(r'^get_detail/$', views.get_detail, name='get_detail'),

    url(r'^upload/$', views.upload, name='upload'),
    url(r'^save_image/$', views.save_image, name='save_image'),

    url(r'^about/$', views.about, name='about'),
    url(r'^issue/$', views.issue, name='issue'),
    url(r'^save_issue/$', views.save_issue, name='save_issue'),
    url(r'^exception/$', views.exception, name='exception'),

    url(r'^editprivate/$', views.editprivate, name='editprivate'),

]
