from rest_framework.authentication import BaseAuthentication
from app01.models import UserInfo, Token
from rest_framework import exceptions


def generate_token(username):
    """生成随机字符串"""
    import hashlib
    import time
    time_str = str(time.time())
    m = hashlib.md5()
    m.update(username.encode('utf8'))
    m.update(time_str.encode('utf8'))
    return m.hexdigest()


class CustomAuthentication(BaseAuthentication):
    """自定义认证类"""

    def authenticate(self, request):
        # 1. 针对get方式请求#################
        # 1.1 一般会携带token值，否则返回login视为匿名用户
        if request._request.method=='GET':
            if not request.query_params.get('token'):
                return (None, None)
            # 1.2 携带错误tk值也视为匿名用户
            token = Token.objects.filter(value= request.query_params.get('token'))
            if token:
                user = token.first().user
                return (user, token)
            return (None, None)

        # 2. 针对post请求#################
        username = request.data.get('username')
        password = request.data.get('password')
        user = UserInfo.objects.filter(username=username, password=password)
        if user:
            token = generate_token(username)
            return (user.first(), token)
        raise exceptions.AuthenticationFailed('用户认证失败')


class Auth(object):
    """用来继承使用自定制的类"""
    authentication_classes = [CustomAuthentication, ]
