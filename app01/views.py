from django.shortcuts import render, HttpResponse
from app01.models import Token
from rest_framework.views import APIView
from app01.utils.my_auth import Auth
from app01.utils.my_throttles import Throttle
from app01.utils.my_permission import Permission


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


class UserSerialize(serializers.Serializer):
    """先建立序列化类"""
    username = serializers.CharField(error_messages={'required': '用户名不能为空'})
    password = serializers.CharField(min_length=4,
                                     error_messages={'required': '密码不能为空','min_length':'不能少于四位'},
                                     validators=[PasswordValidator(),])
    email = serializers.EmailField(error_messages={'required': '邮箱不能为空'})
    user_group = serializers.CharField(source='user_group.title')  # 若存在外键时候，必须指定source参数，否则取出来的是对象
    type = serializers.IntegerField()


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
