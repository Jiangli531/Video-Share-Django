import json
import random
import re

# -*- coding=utf-8
from django.db.models import Max
from datetime import datetime

from django.utils import timezone
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
from UserCommunication.models import VideoPartition, UserLetter
from utils.response_code import SUCCESS
from VideoInteraction.models import LikeRecord
from VideoInteraction.models import Favourites
from UserCommunication.models import UserConnection
from Websurf.models import BrowseRecord
# Create your views here.

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
        # print('上传用户ID:'+uploaderID+'\n')
        test_list = []
        # print(request.POST)
        if UserInfo.objects.filter(userID=uploaderID).exists():
            user = UserInfo.objects.get(userID=uploaderID)
            # print('找到User!')
            if request.session.get('is_login', None):
                VideoInfo.objects.create(videoPath=video_path, videoName=video_title, videoCoverPath=video_cover_path,
                                         videoPart=video_part, videoInformation=video_desc, videoUpUser=user)
                return JsonResponse({'error': SUCCESS, 'msg': '上传成功'})
            else:
                return JsonResponse({'error': 4002, 'msg': '用户未登录'})
        else:
            # print('用户ID：'+uploaderID+'未找到!\n')
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
                    videoUpUser = video.videoUpUser
                    videoUpUser.TotalLikeNum -= video.videoLikeNum  # 用户总点赞数需要更新
                    videoUpUser.TotalPlayNum -= video.videoPlayNum  # 用户总播放数需要更新
                    videoUpUser.save()
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
                try:
                    administrator = UserInfo.objects.get(userID=adminID)
                except:
                    return JsonResponse({'error': 4004, 'msg': '用户不存在'})
                if administrator.userLimit == 1:
                    result = request.POST.get('AuditResult')
                    # audit.auditTime = request.POST.get('AuditTime')
                    audit.auditResult = result
                    audit.auditUser = administrator
                    audit.isAudit = True
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
        userID = request.POST.get('userID')
        if VideoInfo.objects.filter(videoID=videoID, videoUpState=True).exists():
            video = VideoInfo.objects.get(videoID=videoID, videoUpState=True)
            up_user = video.videoUpUser
            videoSrc = video.videoPath
            videoDesc = video.videoInformation
            upID = video.videoUpUser.userID
            upAvatar = video.videoUpUser.userAvatar
            upName = video.videoUpUser.username
            upDesc = video.videoUpUser.userInformation
            uploadDate = video.videoUpTime.strftime('%Y-%m-%d %H:%M')
            videoTitle = video.videoName
            videoLikeNum = video.videoLikeNum
            videoPlayNum = video.videoPlayNum
            videoCommentNum = video.videoCommentNum
            videoFavorNum = video.videoFavorNum
            upUserFansNum = video.videoUpUser.FansNum
            VideoCover = video.videoCoverPath
            try:
                user = UserInfo.objects.get(userID=userID)
                isLiked = LikeRecord.objects.filter(likeUser=user, likeVideo=video).exists()
                isFavored = Favourites.objects.filter(favorUser=user, favorVideo=video).exists()
                isFollowed = UserConnection.objects.filter(followerUser=user, followedUser=up_user).exists()
            except:
                isLiked = False
                isFavored = False
                isFollowed = False
            comment_list = []
            for comment in VideoComment.objects.filter(commentVideo=video):
                commentuser = comment.commentComUser
                user_item = {
                    'id': commentuser.userID,
                    'avatar': commentuser.userAvatar,
                    'nickName': commentuser.username,
                }
                comment_item = {
                    'id': comment.commentID,
                    'commentUser': user_item,
                    'content': comment.commentContent,
                    'createDate': comment.commentTime.strftime('%Y-%m-%d %H:%M'),
                }
                comment_list.append(comment_item)
            return JsonResponse({'error': SUCCESS, 'videoSrc': videoSrc, 'videoDesc': videoDesc,
                                 'videoComment': json.dumps(comment_list, ensure_ascii=False), 'upID': upID,
                                 'upAvatar': upAvatar, 'upName': upName, 'upDesc': upDesc, 'uploadDate': uploadDate,
                                 'videoTitle': videoTitle, 'videoLikeNum': videoLikeNum, 'videoPlayNum': videoPlayNum,
                                    'videoCommentNum': videoCommentNum, 'videoFavorNum': videoFavorNum,
                                    'upUserFansNum': upUserFansNum, 'VideoCover': str(VideoCover), 'isLiked': isLiked,
                                    'isFavored': isFavored, 'isFollowed': isFollowed})
        else:
            return JsonResponse({'error': 4001, 'msg': '视频不存在'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt  # 跨域设置
def getVideoIDByCondition(request):
    if request.method == 'POST':
        video_type = request.POST.get('Type')
        videoID_list = []
        video_part_list = []
        upID_list = []
        video_num = VideoInfo.objects.all().aggregate(Max('videoID'))
        video_num = video_num['videoID__max']
        count = 0
        for video_part in VideoPartition.objects.all():
            part_name = video_part.videoPartName
            video_part_list.append(part_name)
        if video_type == 'Any':
            num_of_video = VideoInfo.objects.filter(videoUpState=True).count()
            if num_of_video == 0:
               return JsonResponse({'error': 4002, 'msg': '没有符合条件的视频'})
            else:
#               while count < num_of_video:
#                   found_id = random.randint(1, video_num)
#                    if VideoInfo.objects.filter(videoID=found_id, videoUpState=True).exists():
#                        video = VideoInfo.objects.get(videoID=found_id, videoUpState=True)
#                        videoID_list.append(video.videoID)
#                        upID_list.append(video.videoUpUser.userID)
#                        count += 1
#                    else:
#                        continue
#                return JsonResponse({'error': SUCCESS, 'videoID': videoID_list, 'upID': upID_list})
                if num_of_video <= 6:
                    for video in VideoInfo.objects.all():
                        videoID_list.append(video.videoID)
                else:
                    while count < 6:
                        found_id = random.randint(1, video_num)
                        if found_id not in videoID_list and VideoInfo.objects.filter(videoID=found_id, videoUpState=True).exists():
                            videoID_list.append(found_id)
                            video = VideoInfo.objects.get(videoID=found_id, videoUpState=True)
                            upID_list.append(video.videoUpUser.userID)  # 上传者ID
                            count += 1
                        else:
                            continue
                return JsonResponse({'error': SUCCESS, 'videoID_list': videoID_list, 'upID_list': upID_list})
        elif video_type == 'Audit':
            num_of_video = AuditRecord.objects.filter(isAudit=False).count()

#            num_of_video = VideoInfo.objects.filter(videoUpState=False).count()
            if num_of_video == 0:
                return JsonResponse({'error': 4002, 'msg': '没有符合条件的视频'})
            else:
                if num_of_video <= 6:
                    for auditRecord in AuditRecord.objects.filter(isAudit=False):
                        if auditRecord.auditVideo.videoUpState and auditRecord.auditVideo.videoID not in videoID_list:
                            videoID_list.append(auditRecord.auditVideo.videoID)
                            upID_list.append(auditRecord.complainedUser.userID)
                            count += 1
                    if count == 0:
                        return JsonResponse({'error': 4002, 'msg': '没有符合条件的视频'})
#                    for video in VideoInfo.objects.filter(videoUpState=False):
#                        videoID_list.append(video.videoID)
#                        upID_list.append(video.videoUpUser.userID)  # 上传者ID
                else:
                    for auditRecord in AuditRecord.objects.filter(isAudit=False):
                        if count >= 6:
                            break
                        if auditRecord.auditVideo.videoUpState and auditRecord.auditVideo.videoID not in videoID_list:
                            videoID_list.append(auditRecord.auditVideo.videoID)
                            upID_list.append(auditRecord.complainedUser.userID)
                            count += 1
                    if count == 0:
                        return JsonResponse({'error': 4002, 'msg': '没有符合条件的视频'})
#                    while count < 6:
#                        found_id = random.randint(1, video_num)
#                        try:
#                            print(found_id)
#                            if (found_id not in videoID_list) and (not VideoInfo.objects.get(videoID=found_id).videoUpState):
#                                videoID_list.append(found_id)
#                                video = VideoInfo.objects.get(videoID=found_id, videoUpState=True)
#                                upID_list.append(video.videoUpUser.userID)  # 上传者ID
#                                count += 1
#                            print(count)
#                        except:
#                            continue
#                        else:
#                            continue
                return JsonResponse({'error': SUCCESS, 'videoID_list': videoID_list, 'upID_list': upID_list})
        elif video_type in video_part_list:
            video_part_need = VideoPartition.objects.get(videoPartName=video_type)
            num_of_video = VideoInfo.objects.filter(videoPart=video_part_need.videoPartName, videoUpState=True).count()
            if num_of_video == 0:
                return JsonResponse({'error': 4002, 'msg': '没有符合条件的视频'})
            else:
                if num_of_video <= 6:
                    for video in VideoInfo.objects.filter(videoPart=video_part_need.videoPartName, videoUpState=True):
                        videoID_list.append(video.videoID)
                        upID_list.append(video.videoUpUser.userID)  # 上传者ID
                else:
                    while count < 6:
                        found_id = random.randint(1, video_num)
                        try:
                            if found_id not in videoID_list and \
                                    VideoInfo.objects.get(videoID=found_id, videoUpState=True).videoPart == video_part_need.videoPartName:
                                videoID_list.append(found_id)
                                video = VideoInfo.objects.get(videoID=found_id, videoUpState=True)
                                upID_list.append(video.videoUpUser.userID)  # 上传者ID
                                count += 1
                        except:
                            continue
                        else:
                            continue
                return JsonResponse({'error': SUCCESS, 'videoID_list': videoID_list, 'upID_list': upID_list})
        else:
            return JsonResponse({'error': 4001, 'msg': 'Type类型错误'})



@csrf_exempt  # 跨域设置
def browseVideo(request):
    if request.method == 'POST':
        videoID = request.POST.get('videoID')
        userID = request.POST.get('userID')
        try:
            video = VideoInfo.objects.get(videoID=videoID, videoUpState=True)
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4001, 'msg': '视频或用户不存在'})
        if BrowseRecord.objects.filter(browseVideo=video, browseUser=user, browseVideoPartition=video.videoPart).exists():
            browser_record = BrowseRecord.objects.get(browseVideo=video, browseUser=user,browseVideoPartition=video.videoPart)
            browser_record.browseTime = timezone.now()
            browser_record.save()
        else:
            BrowseRecord.objects.create(browseVideo=video, browseUser=user, browseVideoPartition=video.videoPart)
        video.videoPlayNum += 1
        video.save()
        video.videoUpUser.TotalPlayNum += 1
        video.videoUpUser.save()
        return JsonResponse({'error': SUCCESS})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt  # 跨域设置
def getAuditInfo(request):
    if request.method == 'POST':
        videoID = request.POST.get('videoID')
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4002, 'msg': '视频不存在'})
        if AuditRecord.objects.filter(auditVideo=video).exists():
            for audit_record in AuditRecord.objects.filter(auditVideo=video):
                if not audit_record.isAudit:
                    auditID = audit_record.auditID
                    complainReason = audit_record.complainReason
                    return JsonResponse({'error': SUCCESS, 'auditID': auditID, 'complainReason': complainReason})
            return JsonResponse({'error': 4003, 'msg': '该视频所有投诉已处理'})
        else:
            return JsonResponse({'error': 4001, 'msg': '视频未在审核中'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def sendResultInfo(request):
    if request.method == 'POST':
        videoID = request.POST.get('videoID')
        adminID = request.POST.get('adminID')
        message = request.POST.get('message')
        try:
            video = VideoInfo.objects.get(videoID=videoID, videoUpState=True)
        except:
            return JsonResponse({'error': 4001, 'msg': '视频不存在'})
        try:
            lettered_user = video.videoUpUser
            letter_user = UserInfo.objects.get(userID=adminID)
        except:
            return JsonResponse({'error': 4002, 'msg': '用户不存在'})

        message = message+' 视频标题：'+video.videoName
        # print(message)
        UserLetter.objects.create(letterUser=letter_user, letteredUser=lettered_user, letterText=message)
        return JsonResponse({'error': 0, 'msg': '通知发送成功'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})