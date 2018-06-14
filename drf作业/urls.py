from django.conf.urls import url, include
from app01.views import LoginView, OrderView, ParserView, \
    SerializeView, test1, test2, test3, index, PageView, create, UserViewSet, UserViewSet3, OperateView,UserViewSet1


urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    # url(r'^index/', IndexView.as_view()),
    url(r'^order/', OrderView.as_view()),

    url(r'^parse/', ParserView.as_view()),
    url(r'^ser/', SerializeView.as_view()),

    # django反向生成url
    url(r'^test1/', test1, name='test1'),
    url(r'^home/', index),
    url(r'^test2/(\d+)/(\d+)', test2, name='test2'),
    url(r'^test3/(?P<k1>\d+)/(?P<k2>\d+)', test3, name='test3'),

    # 分页数据生成
    url(r'^page_num/', PageView.as_view()),
    url(r'^page_limit/', UserViewSet.as_view()),
    url(r'^page_cursor/', UserViewSet3.as_view()),

    # 批量创建用户，准备数据
    url(r'^create/', create),


    ################## 手动操作，增删改查的路由配置
    # 查询所有
    url(r'^operate/$', OperateView.as_view()),
    url(r'^operate\.(?P<format>\w+)$', OperateView.as_view()),
    # 按条件查询（get）\删除(put)、修改(delete)
    url(r'^operate/(?P<pk>\d+)/$', OperateView.as_view()),
    url(r'^operate/(?P<pk>\d+)\.(?P<format>\w+)$', OperateView.as_view()),

    ################## 半自动操作，增删改查的路由配置，
    # 实现查询所有数据列表 和 增加数据
    url(r'^op1/$', UserViewSet1.as_view({'get': 'list', 'post': 'create'})),

    # 实现 查询单一数据 、修改数据、删除数据
    url(r'^op1/(?P<pk>\d+)/$', UserViewSet1.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]

################## 全自动操作，增删改查的路由配置，
from rest_framework import routers

from app01.views import UserViewSet2
router = routers.DefaultRouter()
router.register(r'op3',UserViewSet2)

urlpatterns += [
    url(r'^', include(router.urls)),
]



################## 渲染相关， 根据 用户请求URL 或 用户可接受的类型，筛选出合适的 渲染组件。

from django.conf.urls import url
from app01.views import TestView

urlpatterns += [
    url(r'^test/$', TestView.as_view()),
    url(r'^test\.(?P<format>[a-z0-9]+)', TestView.as_view()),
]













