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
from UserCommunication.models import *


@csrf_exempt
def search(request):
    if request.method == 'POST':
        search_key = request.POST.get('key')
        if search_key:
            user_results = UserInfo.objects.filter(username__icontains=search_key)
            video_results = VideoInfo.objects.filter(videoName__icontains=search_key, videoUpState=True)
            if not user_results and not video_results:
                return JsonResponse({'error': SearchStatus.NO_DATA_ERROR, 'msg': '没有搜索到数据'})
            else:
                user_list = []
                video_list = []
                if user_results:
                    for user in list(user_results):
                        user_item = {
                            'userID': user.userID,
                            'username': user.username,
                            'userInformation': user.userInformation,
                            'userPortrait': user.userAvatar,
                        }
                        # if user.userPortrait:
                        #     user_item['userPortrait'] = str(user.userPortrait.url)
                        # else:
                        #     user_item['userPortrait'] = rootUrl.IMAGE_URL
                        user_list.append(user_item)
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


@csrf_exempt
def getUserInfoByID(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        if UserInfo.objects.filter(userID=userID).exists():
            user = UserInfo.objects.get(userID=userID)
            user_video_num = VideoInfo.objects.filter(videoUpUser=user).count()
            user_info = {
                'userAvatar': user.userAvatar,
                'username': user.username,
                'userDesc': user.userInformation,
                'userFansNum': user.FansNum,
                'userVideosNum': user_video_num,
                'userFollowNum': user.ConcernsNum,
            }
            return JsonResponse({'error': SUCCESS, 'user_info': json.dumps(user_info, ensure_ascii=False)})
        else:
            return JsonResponse({'error': 4001, 'msg': '用户不存在'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方法错误'})


@csrf_exempt
def getConnectionInfoByID(request):
    if request.method == 'POST':
        userAID = request.POST.get('userAID')
        userBID = request.POST.get('userBID')
        try:
            userA = UserInfo.objects.get(userID=userAID)
            userB = UserInfo.objects.get(userID=userBID)
        except:
            return JsonResponse({'error': 4001, 'msg': '用户A或用户B不存在'})
        if UserConnection.objects.filter(followerUser=userA, followedUser=userB).exists():
            hasFollowed = True
        else:
            hasFollowed = False
        return JsonResponse({'error': SUCCESS, 'hasFollowed': hasFollowed})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方法错误'})


@csrf_exempt
def webInfo(request):
    if request.method == 'GET':
        video_sum = VideoInfo.objects.all().count()
        up_sum = VideoInfo.objects.values('videoUpUser').distinct().count()
        user_sum = UserInfo.objects.all().count()
        audit_sum = UserInfo.objects.filter(userLimit=True).count()
        return JsonResponse({'error': SUCCESS, 'videoSum': video_sum, 'upSum': up_sum, 'auditSum':audit_sum,
                             'userSum': user_sum})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方法错误'})
