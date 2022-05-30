import json

from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from VideoManager.models import *
from Video_Share_Django.settings import WEB_ROOT
from Weblogin.models import *
from utils.response_code import *
from utils.Global import *

@csrf_exempt
def search(request):
    if request.method == 'POST':
        search_key = request.POST.get('key')
        if search_key:
            user_results = UserInfo.objects.filter(username__icontains=search_key)
            video_results = VideoInfo.objects.filter(videoName__icontains=search_key)
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
                            'userPortrait': user.userAvatar,
                        }
                        # if user.userPortrait:
                        #     user_item['userPortrait'] = str(user.userPortrait.url)
                        # else:
                        #     user_item['userPortrait'] = rootUrl.IMAGE_URL
                        # user_list.append(user_item)
                if video_results:
                    for video in list(video_results):
                        video_item = {
                            'videoName': video.videoName,
                            'videoCoverPath': str(video.videoCoverPath),
                            'videoPlayNum': video.videoPlayNum,
                            'videoPath': video.videoPath,
                            'videoCommentNum': video.videoCommentNum,
                        }
                        video_list.append(video_item)
                return JsonResponse({'error': SUCCESS, 'user_list': json.dumps(user_list, ensure_ascii=False), 'video_list': json.dumps(video_list, ensure_ascii=False)})
        else:
            return JsonResponse({'error': SearchStatus.NO_KEY_ERROR, 'msg': '搜索内容不能为空'})
    else:
        return JsonResponse({'error': DEFAULT, 'msg': '请求方法错误'})