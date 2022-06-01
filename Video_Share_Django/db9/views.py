from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from db9.models import User
# Create your views here.

@csrf_exempt
def findalluser(get):
    userlist = []
    for user in User.objects.all():
        user_item = {
            'uid': user.uid,
            'uname': user.uname,
            'age': user.age,
            'phone': user.phone,
            'city': user.city,
        }
        userlist.append(user_item)
    return JsonResponse({'status': '200', 'data': userlist})

@csrf_exempt
def AddUser(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        User.objects.create(uname=uname, age=age, phone=phone, city=city)
        return JsonResponse({'error': 0, 'msg': '添加成功'})


@csrf_exempt
def DeleteUser(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        User.objects.filter(uname=uname).delete()
        return JsonResponse({'error': 0, 'msg': '删除成功'})


@csrf_exempt
def UpdateUser(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        User.objects.filter(uname=uname).update(age=age, phone=phone, city=city)
        return JsonResponse({'error': 0, 'msg': '修改成功'})

@csrf_exempt
def FindUser(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        user = User.objects.filter(uname=uname).first()
        if user:
            return JsonResponse({'error': 0, 'msg': '查询成功', 'uname': user.uname, 'age': user.age, 'phone': user.phone,
                                 'city': user.city})
        else:
            return JsonResponse({'error': 1, 'msg': '查询失败'})
