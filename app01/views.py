from django.shortcuts import render, HttpResponse
from app01.models import Token
from rest_framework.views import APIView
from app01.utils.my_auth import Auth
from app01.utils.my_throttles import Throttle
from app01.utils.my_permission import Permission

def create(request):
    user_list = []
    for i in range(100):
        user_list.append(UserInfo(username='alex%s'%i,password='abc%s'%i,email='abc%s@qq.com'%i,))
    UserInfo.objects.bulk_create(user_list)

    return HttpResponse('done！')



class LoginView(Auth, APIView):
    """
    无限制，用户登录后更新或创建token值
    """

    def get(self, request):
        self.dispatch
        return HttpResponse('登录页面')

    def post(self, request):
        Token.objects.update_or_create(user=request.user, defaults={'value': request._auth})
        return HttpResponse('登录页面')


class IndexView(Auth, Throttle, APIView):
    """
    所有人都能访问
    节流：匿名用户10/m, 登录用户20/m
    """

    def get(self, request):
        print('permission_classes', self.throttle_classes)
        print(request.user)
        return HttpResponse('网站首页')


class OrderView(Auth, Permission, Throttle, APIView):
    """
    必须登录查看
    节流：20/m
    """

    def get(self, request):
        return HttpResponse('订单页面')


######################### 解析器

class ParserView(APIView):
    def get(self, request, *args, **kwargs):
        self.dispatch
        print(self.content_negotiation_class)
        print(self.parser_classes)
        return HttpResponse('...')

    def post(self, request, *args, **kwargs):
        print(self.parser_classes)
        print(request.data)
        return HttpResponse('...')


##################### 序列化 ########################
from app01 import models
from rest_framework import serializers
from rest_framework.response import Response


class PasswordValidator(object):
    # def __init__(self, base):
    #     self.base = base  #
    def __call__(self, value):
        # if value != self.base:
        if str(value).isdigit() or str(value).isalpha():
            message = '密码不能只为数字或字母'
            raise serializers.ValidationError(message)

    # def set_context(self, serializer_field):
    #     # 执行验证之前调用,serializer_fields是当前字段对象
    #     pass


############# 手动自定义Serialize类进行验证， 推荐手动写
class UserSerialize(serializers.Serializer):
    """先建立序列化类"""
    username = serializers.CharField(error_messages={'required': '用户名不能为空'})
    password = serializers.CharField(min_length=4,
                                     error_messages={'required': '密码不能为空','min_length':'不能少于四位'},
                                     validators=[PasswordValidator(),])
    email = serializers.EmailField(error_messages={'required': '邮箱不能为空'})
    user_group = serializers.CharField(source='user_group.title')  # 若存在外键时候，必须指定source参数，否则取出来的是对象
    type = serializers.IntegerField()


############# 不推荐，基于model自动生成字段并进行序列化验证
# class UserSerialize(serializers.ModelSerializer):
#     """先建立序列化类"""
#     # 可以手动复写或增加字段
#     user_group = serializers.CharField(source='user_group.title')  # 若存在外键时候，必须指定source参数，否则取出来的是对象
#     class Meta:
#         model = models.UserInfo
#         fields = "__all__"
#         extra_kwargs = {
#             'username': {'min_length':4},
#             'password': {'validators': [PasswordValidator(),]}
#         }


class SerializeView(APIView):

    def get(self, request, *args, **kwargs):
        # 从数据库取出数据并以json返回
        user_list = models.UserInfo.objects.all()
        ser = UserSerialize(instance=user_list, many=True, context={'request': request})
        # user = models.UserInfo.objects.all().first()
        # ser = UserSerialize(instance=user, many=False)
        return Response(ser.data)  # 返回到前端就是json对象

    def post(self, request, *args, **kwargs):
        # 从前端接收数据并验证
        ser = UserSerialize(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
            print(request.data)
            return Response(ser.validated_data)
        else:
            return Response(ser.errors)



##### 在后端利用urls的name属性反向生成url，可以传入参数（位置参数和字符串参数都可以）
##### 在前端也可以利用url的name属性

from django.shortcuts import redirect
from django.urls import reverse

def test1(request):
    # u1 = reverse(viewname='test2',args=(11,22))
    # u1 = reverse(viewname='test2',args=(11,22))
    # print(u1)
    u2 = reverse(viewname='test3',kwargs={'k1':111, 'k2':222})
    print(u2)
    return redirect(u2)

    return HttpResponse('<h1>test1</h1>')

def test2(request, *args):
    print(args)  # ('11', '22')
    return HttpResponse('<h1>test2</h1>')

def test3(request, **kwargs):
    print(kwargs)
    return HttpResponse('<h1>test3</h1>')

def index(request):
    return render(request, 'index.html')




#########################  分页  #################################

from app01.models import UserInfo
from rest_framework.pagination import PageNumberPagination


#####  方法1，记录当前访问的页数数据， /?page=1&page_size=n
class StandardResultsSetPagination(PageNumberPagination):
        # 默认每页显示的数据条数
    page_size = 10
        # 获取URL参数中设置的每页显示数据条数
    page_size_query_param = 'page_size'
        # 获取URL参数中传入的页码key
    page_query_param = 'page'
        # 最大支持的每页显示的数据条数
    max_page_size = 10


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


class PageView(APIView):
    def get(self, request, *args, **kwargs):
        user_list = UserInfo.objects.all().order_by('id')
        paginator = StandardResultsSetPagination()  # 实例化对象
        page_user_list = paginator.paginate_queryset(user_list, self.request, view=self)
        # 序列化对象
        serializer = UserSerializer(page_user_list, many=True)
        # 生成分页和数据
        response = paginator.get_paginated_response(serializer.data)
        return response


#####  方法2，根据offset和limit进行份分页 /?limit=10 & offset=40
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class StandardResultsSetPagination(LimitOffsetPagination):
    # 默认每页显示的数据条数
    default_limit = 10
    # URL中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # URL中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显得条数
    max_limit = None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"

class UserViewSet(APIView):
    def get(self, request, *args, **kwargs):
        user_list = models.UserInfo.objects.all().order_by('id')

        # 实例化分页对象，获取数据库中的分页数据
        paginator = StandardResultsSetPagination()
        page_user_list = paginator.paginate_queryset(user_list, self.request, view=self)

        # 序列化对象
        serializer = UserSerializer(page_user_list, many=True)

        # 生成分页和数据
        response = paginator.get_paginated_response(serializer.data)
        return response


#####  方法3: 无法跳转至某一页，当数据量很大时候，采用此方式分页会较快，因为不存在逐个遍历， /?cursor=cD0xNg%3D%3D

from rest_framework.views import APIView
from rest_framework import serializers

from rest_framework.pagination import CursorPagination

class StandardResultsSetPagination(CursorPagination):
    # URL传入的游标参数
    cursor_query_param = 'cursor'
    # 默认每页显示的数据条数
    page_size = 4
    # URL传入的每页显示条数的参数
    page_size_query_param = 'page_size'
    # 每页显示数据最大条数
    max_page_size = 4
    # 根据ID从大到小排列
    ordering = "id"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


class UserViewSet3(APIView):
    def get(self, request, *args, **kwargs):
        user_list = models.UserInfo.objects.all().order_by('id')

        # 实例化分页对象，获取数据库中的分页数据
        paginator = StandardResultsSetPagination()
        page_user_list = paginator.paginate_queryset(user_list, self.request, view=self)

        # 序列化对象
        serializer = UserSerializer(page_user_list, many=True)

        # 生成分页和数据
        response = paginator.get_paginated_response(serializer.data)
        return response



