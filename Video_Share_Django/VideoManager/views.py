import json
import re

# -*- coding=utf-8
from django.views.decorators.csrf import csrf_exempt
# from qcloud_cos import CosConfig
# from qcloud_cos import CosS3Client
import sys
import logging
from django.http import JsonResponse
from django.shortcuts import render
from utils import response_code
from VideoManager.models import VideoInfo
from Weblogin.models import UserInfo
from VideoManager.models import AuditRecord
from VideoInteraction.models import VideoComment
# Create your views here.
from utils.response_code import SUCCESS


@csrf_exempt  # 跨域设置
def uploadvideo(request):
    if request.method == 'POST':
        video_path = request.POST.get('videoPath')
        video_title = request.POST.get('videoTitle')
        video_cover_path = request.POST.get('videoCoverPath')
        video_part = request.POST.get('videoPart')
        video_desc = request.POST.get('videoDesc')
        uploaderID = request.POST.get('uploaderID')
        # videouptime = request.POST.get('videoUpTime')
        print('上传用户ID:'+uploaderID+'\n')
        test_list = []
        print(request.POST)
        if UserInfo.objects.filter(userID=uploaderID).exists():
            user = UserInfo.objects.get(userID=uploaderID)
            print('找到User!')
            if request.session.get('is_login', None):
                VideoInfo.objects.create(videoPath=video_path, videoName=video_title, videoCoverPath=video_cover_path,
                                         videoPart=video_part, videoInformation=video_desc, videoUpUser=user)
                return JsonResponse({'error': SUCCESS, 'msg': '上传成功'})
            else:
                return JsonResponse({'error': 4002, 'msg': '用户未登录'})
        else:
            print('用户ID：'+uploaderID+'未找到!\n')
            return JsonResponse({'error': 4001, 'msg': '用户不存在'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt  # 跨域设置
def deletevideo(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        if UserInfo.objects.filter(userID=userID).exists() and VideoInfo.objects.filter(videoID=videoID).exists():
            user = UserInfo.objects.get(userID=userID)
            video = VideoInfo.objects.get(videoID=videoID)
            if request.session.get('is_login', None):
                if video.videoUpUser.userID == user.userID or user.userLimit:
                    VideoInfo.objects.get(videoID=videoID).delete()
                    return JsonResponse({'error': SUCCESS, 'msg': '删除成功'})
                else:
                    return JsonResponse({'error': 4003, 'msg': '用户无权限'})
            else:
                return JsonResponse({'error': 4002, 'msg': '用户未登录'})
        else:
            return JsonResponse({'error': 4001, 'msg': '用户不存在或视频不存在'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt  # 跨域设置
def auditvideo(request):
    if request.method == 'POST':
        auditID = request.POST.get('AuditID')
        if AuditRecord.objects.filter(auditID=auditID).exists():
            audit = AuditRecord.objects.get(auditID=auditID)
            if request.session.get('is_login', None):
                adminID = request.POST.get('AdministratorID')
                administrator = UserInfo.objects.get(userID=adminID)
                if administrator.userLimit == 1:
                    result = request.POST.get('AuditResult')
                    # audit.auditTime = request.POST.get('AuditTime')
                    audit.auditResult = result
                    audit.auditUser = administrator
                    audit.save()
                    if not result:
                        audit.auditVideo.videoUpState = False
                        audit.auditVideo.save()
                        return JsonResponse({'error': SUCCESS, 'msg': '审核成功'})
                else:
                    return JsonResponse({'error': 4003, 'msg': '用户无管理员权限'})
            else:
                return JsonResponse({'error': 4002, 'msg': '用户未登录'})
        else:
            return JsonResponse({'error': 4001, 'msg': '审核记录不存在'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt  # 跨域设置
def getVideoByID(request):
    if request.method == 'POST':
        videoID = request.POST.get('videoID')
        if VideoInfo.objects.filter(videoID=videoID).exists():
            video = VideoInfo.objects.get(videoID=videoID)
            videoSrc = video.videoPath
            videoDesc = video.videoInformation
            upAvatar = video.videoUpUser.userPortrait
            upName = video.videoUpUser.username
            upDesc = video.videoUpUser.userInformation
            uploadDate = video.videoUpTime
            videoTitle = video.videoName
            videoLikeNum = video.videoLikeNum
            videoPlayNum = video.videoPlayNum
            videoCommentNum = video.videoCommentNum
            videoFavorNum = video.videoFavorNum
            upUserFansNum = video.videoUpUser.FansNum
            VideoCover = video.videoCoverPath
            comment_list = []
            for comment in VideoComment.objects.filter(commentVideo=video):
                commentuser = comment.commentComUser
                user_item = {
                    'id': commentuser.userID,
                    'nickname': commentuser.username,
                    'avatar': str(commentuser.userPortrait),
                }
                comment_item = {
                    'id': comment.commentID,
                    'commentUser': user_item,
                    'content': comment.commentContent,
                    'createDate': str(comment.commentTime),
                }
                comment_list.append(comment_item)
            return JsonResponse({'error': SUCCESS, 'videoSrc': videoSrc, 'videoDesc': videoDesc,
                                 'videoComment': json.dumps(comment_list, ensure_ascii=False), 'upAvatar': str(upAvatar),
                                 'upName': upName, 'upDesc': upDesc, 'uploadDate': str(uploadDate),
                                 'videoTitle': videoTitle, 'videoLikeNum': videoLikeNum, 'videoPlayNum': videoPlayNum,
                                    'videoCommentNum': videoCommentNum, 'videoFavorNum': videoFavorNum,
                                    'upUserFansNum': upUserFansNum, 'VideoCover': str(VideoCover)})
        else:
            return JsonResponse({'error': 4001, 'msg': '视频不存在'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


#@csrf_exempt  # 跨域设置
#def getVideoIDByCondition(request):
    #if request.method == 'POST':
        #video_type = request.POST.get('Type')
        #if video_type == 'Any':

