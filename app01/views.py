from django.shortcuts import render, HttpResponse
from app01.models import Token
from rest_framework.views import APIView
from app01.utils.my_auth import Auth
from app01.utils.my_throttles import Throttle
from app01.utils.my_permission import Permission

class LoginView(Auth,APIView):
    """
    无限制，用户登录后更新或创建token值
    """
    def get(self, request):
        self.dispatch
        return HttpResponse('登录页面')

    def post(self, request):
        Token.objects.update_or_create(user=request.user, defaults={'value': request._auth})
        return HttpResponse('登录页面')


class IndexView(Auth,Throttle,APIView):
    """
    所有人都能访问
    节流：匿名用户10/m, 登录用户20/m
    """
    def get(self, request):
        print('permission_classes', self.throttle_classes)
        print(request.user)
        return HttpResponse('网站首页')


class OrderView(Auth,Permission,Throttle,APIView):
    """
    必须登录查看
    节流：20/m
    """
    def get(self, request):
        return HttpResponse('订单页面')






