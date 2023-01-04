from django.http import HttpResponse
from rest_framework import status as status_code
from main_project.settings import SECRET_KEY, FunctionDonotNeedAuth
from core.models import User
import jwt
import json
import re


class auth:
    def __init__(self, get_response):
        print('init django middleware')
        self.get_response = get_response

    def __return(self, code: status_code, message: str) -> HttpResponse:
        return HttpResponse(json.dumps({'data': {'code': code, 'message': message}}), status=code)

    def __call__(self, request):
        # notNeed is return (notNeed >= 1) if the request not need an auth
        print('ok')
        print(request.path)
        notNeed = sum(
            map(lambda item: request.body.find(item), FunctionDonotNeedAuth))
        if not (request.path == '/graphql/') or notNeed > 0 or request.body == b'':
            print('no need auth')
            return self.get_response(request)
        # extract data from header
        regex = re.compile('^HTTP_')
        header = dict((regex.sub('', header), value) for (header, value)
                      in request.META.items() if header.startswith('HTTP_'))
        if not 'TOKEN' in header:
            return self.__return(status_code.HTTP_400_BAD_REQUEST, 'there is no token')
        return self.checkToken(header['TOKEN'], request=request)

    def checkToken(self, token, request):
        try:
            request.META.update(decode_token(token))
            print(request.META['user'])
            return self.get_response(request)
        except Exception as e:
            print('Error in checkToken')
            print(e)
            return self.__return(status_code.HTTP_401_UNAUTHORIZED, str(e))


def decode_token(token: str) -> User:
    username = jwt.decode(
        token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.filter(username=username["username"])
    if user.exists():
        return {"user": user.first()}
    else:
        raise Exception(jwt.InvalidTokenError)
