import json

from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from VideoManager.models import *
from Video_Share_Django.settings import WEB_ROOT
from Weblogin.models import *
from utils.response_code import *


def search(request):
    if request.method == 'POST':
        serach_key = request.POST.get('key')
        if serach_key:
            user_results = UserInfo.objects.filter(username__icontains=serach_key)
            video_results = VideoInfo.objects.filter(videoName__icontains=serach_key)
            if not user_results and not video_results:
                return JsonResponse({'error': SearchStatus.NO_DATA_ERROR, 'msg': '没有搜索到数据'})
            else:
                user_list = []
                video_list = []
                if user_results:
                    for user in list(user_results):
                        user_item = {
                            'username': user.username,
                            'userInformation': user.userInformation,
                        }
                        if user.userPortrait:
                            user_item['userPortrait'] = WEB_ROOT + user.userPortrait.url
                        else:
                            user_item['userPortrait'] = WEB_ROOT + '/media/portrait/user_default/' + '1.png'
                        user_list.append(user_item)
                if video_results:
                    for video in list(video_results):
                        video_item = {
                            'videoName': video.videoName,
                            'videoCoverPath' : WEB_ROOT + video.videoCoverPath.url,
                        }
                        video_list.append(video_item)
                return JsonResponse({'error' : SUCCESS, 'user_list': json.dumps(user_list, ensure_ascii=False), 'video_list': json.dumps(video_list, ensure_ascii=False)})
        else:
            return JsonResponse({'error': SearchStatus.NO_KEY_ERROR, 'msg': '搜索内容不能为空'})
    else:
        return JsonResponse({'error': DEFAULT, 'msg': '请求方法错误'})