import re

# -*- coding=utf-8
from django.views.decorators.csrf import csrf_exempt
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
from django.http import JsonResponse
from django.shortcuts import render
from utils import response_code
from VideoManager.models import VideoInfo
from Weblogin.models import UserInfo


# Create your views here.
from utils.response_code import SUCCESS


@csrf_exempt  # 跨域设置
def uploadvideo(request):
    if request.methods == 'POST':
        postform = request.POST
        if postform.is_valid():
            videopath = request.POST.get('videoPath')
            videotitle = request.POST.get('videoTitle')
            videocoverpath = request.POST.get('videoCoverPath')
            videopart = request.POST.get('videoPart')
            videodesc = request.POST.get('videoDesc')
            uploaderid = request.POST.get('uploaderID')
            videouptime = request.POST.get('videoUpTime')
            if UserInfo.objects.filter(userID=uploaderid).exists():
                user = UserInfo.objects.get(userID=uploaderid)
                if request.session.get('is_login', None):
                    VideoInfo.objects.create(videoPath=videopath, videoTitle=videotitle, videoCoverPath=videocoverpath,
                                             videoPart=videopart, videoInformation=videodesc, videoUpUser=user,
                                             videoUpTime=videouptime)
                    return JsonResponse({'error': SUCCESS, 'msg': '上传成功'})
                else:
                    return JsonResponse({'error': 4002, 'msg': '用户未登录'})
            else:
                return JsonResponse({'error': 4001, 'msg': '用户不存在'})
        else:
            return JsonResponse({'error': 3001, 'msg': '表单错误'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})





@csrf_exempt  # 跨域设置
def deletevideo(request):
    if request.methods == 'POST':
        postform = request.POST
        if postform.is_valid():
            userid = request.POST.get('userID')
            videoid = request.POST.get('videoID')
            if UserInfo.objects.filter(userID=userid).exists():
                user = UserInfo.objects.get(userID=userid)
                video = VideoInfo.objects.get(videoID=videoid)
                if request.session.get('is_login', None):
                    if(video.videoUpUser == user):
                        VideoInfo.objects.get(videoID=videoid).delete()
                        return JsonResponse({'error': SUCCESS, 'msg': '删除成功'})
                    else:
                        return JsonResponse({'error': 4003, 'msg': '用户无权限'})
                else:
                    return JsonResponse({'error': 4002, 'msg': '用户未登录'})
            else:
                return JsonResponse({'error': 4001, 'msg': '用户不存在'})
        else:
            return JsonResponse({'error': 3001, 'msg': '表单错误'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


#@csrf_exempt  # 跨域设置
#def auditvideo(request):