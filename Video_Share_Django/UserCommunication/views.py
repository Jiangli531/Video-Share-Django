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
        userid = request.POST.get('userid')
        followeduserid = request.POST.get('followeduserid')
        user = UserInfo.objects.get(userID=userid)
        followeduser = UserInfo.objects.get(userID=followeduserid)
        UserConnection.objects.create(followerUser=user, followedUser=followeduser)
        followeduser.FansNum = followeduser.FansNum + 1
        followeduser.save()
        user.ConcernsNum = user.ConcernsNum + 1
        user.save()
        return JsonResponse({'error': 0, 'msg': "关注成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancelfollow(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        followeduserid = request.POST.get('followeduserid')
        user = UserInfo.objects.get(userID=userid)
        followeduser = UserInfo.objects.get(userID=followeduserid)
        UserConnection.objects.get(followerUser=user, followedUser=followeduser).delete()
        followeduser.FansNum = followeduser.FansNum - 1
        followeduser.save()
        user.ConcernsNum = user.ConcernsNum - 1
        user.save()
        return JsonResponse({'error': 0, 'msg': "取消关注成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def sendletter(request):
    if request.method == 'POST':
        letteruserid = request.POST.get('letteruserid')
        lettereduserid = request.POST.get('lettereduserid')
        lettertext = request.POST.get('lettertext')
        letteruser = UserInfo.objects.get(userID=letteruserid)
        lettereduser = UserInfo.objects.get(userID=lettereduserid)
        if letteruser.userLimit == 1:
            UserLetter.objects.create(letterUser=letteruser, letteredUser=lettereduser, letterText=lettertext)
            return JsonResponse({'error': 0, 'msg': "私信已发送"})
        else:
            return JsonResponse({'error': 4001, 'msg': "该用户无权限发送私信"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def enterhomepage(request):
    if request.method == 'POST':
        entereduserid = request.POST.get('entereduserid')
        entereduser = UserInfo.objects.get(userID=entereduserid)
        username = entereduser.username
        userportrait = entereduser.userPortrait
        userinformation = entereduser.userInformation
        usersex = entereduser.userSex
        userbirthday = entereduser.userBirthday
        fansnum = entereduser.FansNum
        playnum = entereduser.TotalPlayNum
        concernsnum = entereduser.ConcernsNum
        msg_list = []
        msg_item = {
            'userid': entereduserid,
            'username': username,
            'userportrait': str(userportrait),
            'userinformation': userinformation,
            'usersex': usersex,
            'userbirthday': userbirthday,
            'fansnum': fansnum,
            'playnum': playnum,
            'concernsnum': concernsnum,
        }
        msg_list.append(msg_item)
        video_list = []
        for video in list(VideoInfo.objects.filter(videoUpUser=entereduser)):
            video_item = {
                'videoid': video.videoID,
                'videotitle': video.videoTitle,
                'videoplaynum': video.videoPlayNum,
                'videocommentnum': video.videoCommentNum,
                'videouptime': video.videoUpTime,
                'videoupuser': video.videoUpUser.username,
                'videocover': str(video.videoCover),
            }
            video_list.append(video_item)
        fanslist = []
        for user in list(UserConnection.objects.filter(followedUser=entereduser)):
            fans_item = {
                'userid': user.userID,
                'username': user.username,
                'userportrait': str(user.userPortrait),
                'userinformation': user.userInformation,
            }
            fanslist.append(user)

        concernslist = []
        for user in list(UserConnection.objects.filter(followerUser=entereduser)):
            concerns_item = {
                'userid': user.userID,
                'username': user.username,
                'userportrait': str(user.userPortrait),
                'userinformation': user.userInformation,
            }
            concernslist.append(concerns_item)

        favourlist = []
        for favourite in list(Favourites.objects.filter(favorUser=entereduser)):
            video = favourite.favorVideo
            if video.videoUpState == 1:
                favour_item = {
                    'videoid': video.videoID,
                    'videotitle': video.videoTitle,
                    'videoplaynum': video.videoPlayNum,
                    'videocommentnum': video.videoCommentNum,
                    'videocover': str(video.videoCover),
                    'videouptime': video.videoUpTime,
                    'videoupuser': video.videoUpUser.username,
                }
                favourlist.append(favour_item)

        letterlist = []
        for letter in list(UserLetter.objects.filter(letteredUser=entereduser)):
            letter_item = {
                'letteruser': letter.letterUser.username,
                'lettertext': letter.letterText,
                'lettertime': letter.letterTime,
            }
            letterlist.append(letter_item)

        browselist = []
        for browse in list(BrowseRecord.objects.filter(browseUser=entereduser)):
            browse_item = {
                'browsetime': browse.BrowseTime,
                'browsevideotitle': browse.BrowseVideo.videoTitle,
                'browsevideouser': browse.BrowseVideo.videoUpUser.username,
                'browsevideocover': str(browse.BrowseVideo.videoCover),
            }
            browselist.append(browse_item)

        return JsonResponse({'error': SUCCESS, 'msg_list': json.dumps(msg_list, ensure_ascii=False),
                             'video_list': json.dumps(video_list, ensure_ascii=False),
                             'fanslist': json.dumps(fanslist, ensure_ascii=False),
                             'concernslist': json.dumps(concernslist, ensure_ascii=False),
                             'favourlist': json.dumps(favourlist, ensure_ascii=False),
                             'letterlist': json.dumps(letterlist, ensure_ascii=False),
                             'browselist': json.dumps(browselist, ensure_ascii=False)})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
