from django.http import JsonResponse

# status编码表示
# 200 OK：表示请求已经成功处理，并返回相应的结果。
# 201 Created：表示新资源已经成功创建。
# 204 No Content：表示请求已经成功处理，但没有返回任何内容。
# 400 Bad Request：表示请求参数有误或请求格式不正确。
# 401 Unauthorized：表示请求需要用户认证，但用户没有提供有效的认证凭证。
# 403 Forbidden：表示服务器拒绝访问请求的资源，通常是因为用户没有足够的权限。
# 404 Not Found：表示请求的资源不存在或未被找到。
# 405 Method Not Allowed：表示请求方法不被允许，通常是因为请求方法不正确或资源不支持该方法。
# 500 Internal Server Error：表示服务器内部发生了错误，无法完成请求的处理。


class APIResponse(JsonResponse):

    def __init__(self, status, data, error, **kwargs):
        content = {
            'status': status,
            'data': data,
            'error': error
        }
        kwargs.setdefault('safe', False)
        kwargs.setdefault('json_dumps_params', {'ensure_ascii': False})
        super().__init__(content, **kwargs)
