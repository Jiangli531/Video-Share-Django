import re

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Weblogin.models import UserInfo
from UserCommunication.models import UserConnection
from UserCommunication.models import UserLetter


@csrf_exempt  # 跨域设置
def followuser(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        followeduserid = request.POST.get('followeduserid')
        user = UserInfo.objects.get(userID=userid)
        followeduser = UserInfo.objects.get(userID=followeduserid)
        UserConnection.objects.create(followerUser=user, followedUser=followeduser)
        return JsonResponse({'error': 6010, 'msg': "关注成功"})
    else:
        return JsonResponse({'error': 6011, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancelfollow(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        followeduserid = request.POST.get('followeduserid')
        user = UserInfo.objects.get(userID=userid)
        followeduser = UserInfo.objects.get(userID=followeduserid)
        UserConnection.objects.get(followerUser=user, followedUser=followeduser).delete()
        return JsonResponse({'error': 6020, 'msg': "取消关注成功"})
    else:
        return JsonResponse({'error': 6021, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def sendletter(request):
    if request.method == 'POST':
        letteruserid = request.POST.get('letteruserid')
        lettereduserid = request.POST.get('lettereduserid')
        lettertext = request.POST.get('lettertext')
        letteruser = UserInfo.objects.get(userID=letteruserid)
        lettereduser = UserInfo.objects.get(userID=lettereduserid)
        UserLetter.objects.create(letterUser=letteruser, letteredUser=lettereduser, letterText=lettertext)
        return JsonResponse({'error': 6030, 'msg': "私信已发送"})
    else:
        return JsonResponse({'error': 6031, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def enterhomepage(request):
