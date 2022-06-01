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
        try:
            user = UserInfo.objects.get(userID=userID)
            followed_user = UserInfo.objects.get(userID=followed_userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "关注用户或被关注用户不存在"})
        if UserConnection.objects.filter(followerUser=user, followedUser=followed_user).exists():
            return JsonResponse({'error': 4001, 'msg': "您已经关注过了"})
        else:
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
        try:
            user = UserInfo.objects.get(userID=userID)
            followed_user = UserInfo.objects.get(userID=followed_userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "关注用户或被关注用户不存在"})
        if UserConnection.objects.filter(followerUser=user, followedUser=followed_user).exists():
            UserConnection.objects.get(followerUser=user, followedUser=followed_user).delete()
            followed_user.FansNum = followed_user.FansNum - 1
            followed_user.save()
            user.ConcernsNum = user.ConcernsNum - 1
            user.save()
            return JsonResponse({'error': 0, 'msg': "取消关注成功"})
        else:
            return JsonResponse({'error': 4001, 'msg': "您还没有关注过"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def sendletter(request):
    if request.method == 'POST':
        letter_userID = request.POST.get('letterUserID')
        lettered_userID = request.POST.get('letteredUserID')
        letter_text = request.POST.get('letterText')
        try:
            letter_user = UserInfo.objects.get(userID=letter_userID)
            lettered_user = UserInfo.objects.get(userID=lettered_userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "发送用户或接收用户不存在"})
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
        try:
            entered_user = UserInfo.objects.get(userID=entered_userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "该用户不存在"})
        username = entered_user.username
        userportrait = entered_user.userAvatar
        userinformation = entered_user.userInformation
        usersex = entered_user.userSex
        userbirthday = str(entered_user.userBirthday)
        fansnum = entered_user.FansNum
        playnum = entered_user.TotalPlayNum
        concernsnum = entered_user.ConcernsNum
        likenum = entered_user.TotalLikeNum
        msg_list = []
        msg_item = {
            'userID': entered_userID,
            'username': username,
            'userPortrait': userportrait,
            'userInformation': userinformation,
            'userSex': usersex,
            'userBirthday': userbirthday,
            'fansNum': fansnum,
            'playNum': playnum,
            'concernsNum': concernsnum,
            'likeNum': likenum
        }
        msg_list.append(msg_item)
        video_list = []
        for video in list(VideoInfo.objects.filter(videoUpUser=entered_user)):
            video_item = {
                'videoID': video.videoID,
                'videoTitle': video.videoName,
                'videoPlayNum': video.videoPlayNum,
                'videoCommentNum': video.videoCommentNum,
                'videoUpTime': video.videoUpTime.strftime("%Y-%m-%d %H:%M"),
                'videoUpUser': video.videoUpUser.username,
                'videoCover': str(video.videoCoverPath),
            }
            video_list.append(video_item)
        fanslist = []
        for connectInfo_1 in list(UserConnection.objects.filter(followedUser=entered_user)):
            user = connectInfo_1.followerUser
            fans_item = {
                'userID': user.userID,
                'username': user.username,
                'userPortrait': user.userAvatar,
                'userInformation': user.userInformation,
            }
            fanslist.append(fans_item)

        concernslist = []
        for connectInfo_2 in list(UserConnection.objects.filter(followerUser=entered_user)):
            user = connectInfo_2.followedUser
            concerns_item = {
                'userID': user.userID,
                'username': user.username,
                'userPortrait': user.userAvatar,
                'userInformation': user.userInformation,
            }
            concernslist.append(concerns_item)

        favourlist = []
        for favourite in list(Favourites.objects.filter(favorUser=entered_user)):
            video = favourite.favorVideo
            if video.videoUpState == 1:
                favour_item = {
                    'videoID': video.videoID,
                    'videoTitle': video.videoName,
                    'videoPlayNum': video.videoPlayNum,
                    'videoCommentNum': video.videoCommentNum,
                    'videoCover': str(video.videoCoverPath),
                    'videoUpTime': video.videoUpTime.strftime("%Y-%m-%d %H:%M"),
                    'videoUpUser': video.videoUpUser.username,
                }
                favourlist.append(favour_item)

        letterlist = []
        for letter in list(UserLetter.objects.filter(letteredUser=entered_user)):
            letter_item = {
                'letterUser': letter.letterUser.username,
                'letterText': letter.letterText,
                'letterTime': letter.letterTime.strftime("%Y-%m-%d %H:%M"),
            }
            letterlist.append(letter_item)

        browselist = []
        for browse in list(BrowseRecord.objects.filter(browseUser=entered_user)):
            browse_item = {
                'browseTime': browse.BrowseTime.strftime("%Y-%m-%d %H:%M"),
                'browseVideoTitle': browse.BrowseVideo.videoName,
                'browseVideoUser': browse.BrowseVideo.videoUpUser.username,
                'browseVideoCover': str(browse.BrowseVideo.videoCoverPath),
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
