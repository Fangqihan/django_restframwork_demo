
from rest_framework.throttling import SimpleRateThrottle

class AnonThrottle_1(SimpleRateThrottle):
    """针对匿名用户限制访问次数"""
    scope = 'anon'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

    def allow_request(self, request, view):
        """返回true则限制，反之不限制，支持多个限制规则"""
        if request.user:
            # 登录用户不限制
            return True
        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        # 剔除掉时间久远的缓存，直到与当前时间间隔60s以内的
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()


class UserThrottle_1(SimpleRateThrottle):
    """针对登录用户限制访问次数"""
    scope = 'user'

    def get_cache_key(self, request, view):

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

    def allow_request(self, request, view):
        """返回true则限制，反之不限制，支持多个限制规则"""
        if not request.user:
            # 只针对已通过认证的用户
            return True
        self.key = request.user.username
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        # 剔除掉时间久远的缓存，直到与当前时间间隔60s以内的
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()


class Throttle(object):
    throttle_classes = [AnonThrottle_1,UserThrottle_1]

