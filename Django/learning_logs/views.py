from django.shortcuts import render
from .models import activity
import simplejson
import json

from django.http import JsonResponse,HttpResponse,HttpRequest

def reg(request:HttpRequest):
    return HttpResponse("test")

def delete(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)  
        id = payload['id']
        mgr = activity.objects.get(id=id)
        mgr.delete()
        return JsonResponse({'Status': 'DeleteSuccess'})
    except Exception as e:
        return JsonResponse({'Runstatus': e.args})

def update_by_id(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        id = payload['id']
        mgr = activity.objects.filter(id=id)
        name = payload['name']
        cost = payload['cost']
        deposit = payload['deposit']
        activity_price_deposit = payload['activity_price_deposit']
        toplimit = payload['toplimit']
        Statement = payload['Statement']
        ac = activity()
        ac.id = id
        ac.name = name
        ac.cost = cost
        ac.deposit = deposit
        ac.activity_price_deposit = activity_price_deposit
        ac.toplimit = toplimit
        ac.Statement = Statement
        ac.save()
        return JsonResponse({'Status': 'UpDateSucess'})
    except Exception as e:
        return JsonResponse({'Status': 'UpDateError'})

def Select_by_id(request: HttpRequest):
    try:
        payload = json.loads(request.body)
        id = payload['id']
        mgr = activity.objects.get(id=id)
        data={
            'name': mgr.name,
            'cost': mgr.cost,
            'deposit' : mgr.deposit,
            'activity_price_deposit': mgr.activity_price_deposit,
            'toplimit': mgr.toplimit,
            'Statement': mgr.Statement
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'Runstatus':e.args})

def Create(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        id = payload['id']
        mgr = activity.objects.filter(id=id)
        if mgr:  # 如果数据库中存在
            return JsonResponse({'Status': 'Exist'})
        else:
            name = payload['name']
            cost=payload['cost']
            deposit=payload['deposit']
            activity_price_deposit=payload['activity_price_deposit']
            toplimit=payload['toplimit']
            Statement=payload['Statement']
            ac = activity()
            ac.id = id
            ac.name = name
            ac.cost=cost
            ac.deposit=deposit
            ac.activity_price_deposit=activity_price_deposit
            ac.toplimit=toplimit
            ac.Statement=Statement
            ac.save()
            return JsonResponse({'Status': 'CreateSucess'})

    except Exception as e:
        return JsonResponse({'Status': 'CreateError'})
