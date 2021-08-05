from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
import time

# Create your views here.
def index(request):
    # print('path',request.path)
    print('method',request.method)
    # print('POST',request.POST)
    # body = request.body.decode()
    # print('body',body) # 获得json形式字符串
    # body = json.loads(body)
    # print('body',body) # json dict
    # print('META',request.META)
    print('request', type(request))
    print('host', request.get_host())  # 服务端ip
    print('client', request.META['REMOTE_ADDR'])

    res = {'name': 'wc', 'item': 123}
    return JsonResponse(data=res, safe=False)

def set_cookie(request):
  
    username = request.GET.get("username")
    request.session['user_id'] = 1
    request.session['user_name'] = username
    response = HttpResponse('set_cookie')
    response.set_cookie('name', username)
    return response


def get_session(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    content = '{},{}'.format(user_id, user_name)
    return HttpResponse(content)


class UsernameCountView(View):
    def get(self, request):
        print('method',request.method)
        name = request.GET.get("name")
        return JsonResponse({'res': name})
    
    def post(self,request):
        print('method',request.method)
        return JsonResponse({'res':0})        
    def put(self,request):
        print('method',request.method)
        return JsonResponse({'res':1})  
    def delete(self,request):
        print('method',request.method)
        return JsonResponse({'res':2})  
              
