"""drf作业 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from app01.views import LoginView, IndexView, OrderView, ParserView, SerializeView,test1, test2, test3,index


urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    # url(r'^index/', IndexView.as_view()),
    url(r'^order/', OrderView.as_view()),

    url(r'^parse/', ParserView.as_view()),
    url(r'^ser/', SerializeView.as_view()),

    # django反向生成url

    url(r'^test1/', test1, name='test1'),
    url(r'^index/', index),
    url(r'^test2/(\d+)/(\d+)', test2, name='test2'),
    url(r'^test3/(?P<k1>\d+)/(?P<k2>\d+)', test3, name='test3'),


]
