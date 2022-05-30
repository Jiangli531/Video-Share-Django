import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Weblogin.models import UserInfo
from UserCommunication.models import UserConnection
from UserCommunication.models import UserLetter
from utils.response_code import SUCCESS
from VideoInteraction.models import Favourites
from VideoManager.models import VideoInfo
from Websurf.models import BrowseRecord

@csrf_exempt  # 跨域设置
def followuser(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        followed_userID = request.POST.get('followedUserID')
        user = UserInfo.objects.get(userID=userID)
        followed_user = UserInfo.objects.get(userID=followed_userID)
        UserConnection.objects.create(followerUser=user, followedUser=followed_user)
        followed_user.FansNum = followed_user.FansNum + 1
        followed_user.save()
        user.ConcernsNum = user.ConcernsNum + 1
        user.save()
        return JsonResponse({'error': 0, 'msg': "关注成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancelfollow(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        followed_userID = request.POST.get('followedUserID')
        user = UserInfo.objects.get(userID=userID)
        followed_user = UserInfo.objects.get(userID=followed_userID)
        UserConnection.objects.get(followerUser=user, followedUser=followed_user).delete()
        followed_user.FansNum = followed_user.FansNum - 1
        followed_user.save()
        user.ConcernsNum = user.ConcernsNum - 1
        user.save()
        return JsonResponse({'error': 0, 'msg': "取消关注成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def sendletter(request):
    if request.method == 'POST':
        letter_userID = request.POST.get('letterUserID')
        lettered_userID = request.POST.get('letteredUserID')
        letter_text = request.POST.get('letterText')
        letter_user = UserInfo.objects.get(userID=letter_userID)
        lettered_user = UserInfo.objects.get(userID=lettered_userID)
        if letter_user.userLimit == 1:
            UserLetter.objects.create(letterUser=letter_user, letteredUser=lettered_user, letterText=letter_text)
            return JsonResponse({'error': 0, 'msg': "私信已发送"})
        else:
            return JsonResponse({'error': 4001, 'msg': "该用户无权限发送私信"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def enterhomepage(request):
    if request.method == 'POST':
        entered_userID = request.POST.get('enteredUserID')
        entered_user = UserInfo.objects.get(userID=entered_userID)
        username = entered_user.username
        userportrait = entered_user.userPortrait
        userinformation = entered_user.userInformation
        usersex = entered_user.userSex
        userbirthday = entered_user.userBirthday
        fansnum = entered_user.FansNum
        playnum = entered_user.TotalPlayNum
        concernsnum = entered_user.ConcernsNum
        msg_list = []
        msg_item = {
            'userID': entered_userID,
            'username': username,
            'userPortrait': str(userportrait),
            'userInformation': userinformation,
            'userSex': usersex,
            'userBirthday': userbirthday,
            'fansNum': fansnum,
            'playNum': playnum,
            'concernsNum': concernsnum,
        }
        msg_list.append(msg_item)
        video_list = []
        for video in list(VideoInfo.objects.filter(videoUpUser=entered_user)):
            video_item = {
                'videoID': video.videoID,
                'videoTitle': video.videoTitle,
                'videoPlayNum': video.videoPlayNum,
                'videoCommentNum': video.videoCommentNum,
                'videoUpTime': video.videoUpTime,
                'videoUpUser': video.videoUpUser.username,
                'videoCover': str(video.videoCover),
            }
            video_list.append(video_item)
        fanslist = []
        for user in list(UserConnection.objects.filter(followedUser=entereduser)):
            fans_item = {
                'userID': user.userID,
                'username': user.username,
                'userPortrait': str(user.userPortrait),
                'userInformation': user.userInformation,
            }
            fanslist.append(user)

        concernslist = []
        for user in list(UserConnection.objects.filter(followerUser=entereduser)):
            concerns_item = {
                'userID': user.userID,
                'username': user.username,
                'userPortrait': str(user.userPortrait),
                'userInformation': user.userInformation,
            }
            concernslist.append(concerns_item)

        favourlist = []
        for favourite in list(Favourites.objects.filter(favorUser=entereduser)):
            video = favourite.favorVideo
            if video.videoUpState == 1:
                favour_item = {
                    'videoID': video.videoID,
                    'videoTitle': video.videoTitle,
                    'videoPlayNum': video.videoPlayNum,
                    'videoCommentNum': video.videoCommentNum,
                    'videoCover': str(video.videoCover),
                    'videoUpTime': video.videoUpTime,
                    'videoUpUser': video.videoUpUser.username,
                }
                favourlist.append(favour_item)

        letterlist = []
        for letter in list(UserLetter.objects.filter(letteredUser=entereduser)):
            letter_item = {
                'letterUser': letter.letterUser.username,
                'letterText': letter.letterText,
                'letterTime': letter.letterTime,
            }
            letterlist.append(letter_item)

        browselist = []
        for browse in list(BrowseRecord.objects.filter(browseUser=entereduser)):
            browse_item = {
                'browseTime': browse.BrowseTime,
                'browseVideoTitle': browse.BrowseVideo.videoTitle,
                'browseVideoUser': browse.BrowseVideo.videoUpUser.username,
                'browseVideoCover': str(browse.BrowseVideo.videoCover),
            }
            browselist.append(browse_item)

        return JsonResponse({'error': SUCCESS, 'msg_list': json.dumps(msg_list, ensure_ascii=False),
                             'video_list': json.dumps(video_list, ensure_ascii=False),
                             'fans_list': json.dumps(fanslist, ensure_ascii=False),
                             'concerns_list': json.dumps(concernslist, ensure_ascii=False),
                             'favour_list': json.dumps(favourlist, ensure_ascii=False),
                             'letter_list': json.dumps(letterlist, ensure_ascii=False),
                             'browse_list': json.dumps(browselist, ensure_ascii=False)})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
