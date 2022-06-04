"""
枚举类：定义状态码，用于前后端传输
"""

SUCCESS = 0
DEFAULT = 2001  # 没发送请求或发送请求类型不对
FORM_ERROR = 3001  # 表单信息错误（未全部填写或数据类型有误）

# 系统错误
PAGE_NOT_FOUND = 404


# Wrong

#Weblogin Part
class LoginStatus:  #WebLogin.login
    LOGIN_REPEATED = 4001  # 用户已登录
    EMAIL_MISS = 4002  # 邮箱不存在
    PASSWORD_ERROR = 4003  # 密码错误
    USER_NOT_CONFIRM = 4004  # 用户未通过邮件验证



class RegisterStatus:  #Weblogin.register
    USERNAME_REPEATED = 4001  # 用户名已存在
    EMAIL_ERROR = 4002  # 邮箱已存在
    PASSWORD_INVALID = 4003  # 密码不符合规则，应至少同时包含字母和数字，且长度为 8-18
    PASSWORD_CONTRAST = 4004  # 两次输入的密码不同
    SEND_EMAIL_ERROR = 4005  # 邮件验证码发送失败


class LogoutStatus:   #Weblogin.logout
    USER_NOT_LOGIN = 4001  # 用户未登录


class ConfirmStatus:  #Weblogin.user_confirm
    STRING_MISS = 4001  # 验证码不存在，即返回无效的确认请求
    CONFIRM_EXPIRED = 4002  # 验证码已过期，请重新注册


class ForgetPasswordStatus:   #Weblogin.forget_pwd
    SEND_EMAIL_ERROR = 4001 #邮件发送失败
    EMAIL_MISS = 4002 #邮箱还未注册


class PasswordUpdateStatus:   #Weblogin.update_pwd
    PASSWORD_INVALID = 4001 #密码不符合规范
    STRING_ERROR = 4002 #验证码错误


#Websurf Part
class SearchStatus:
    USER_NOT_EXISTS = 4001  # 用户不存在
    VIDEO_NOT_EXISTS = 4002  # 视频不存在
    NO_KEY_ERROR = 4003  # 检索关键词为空
    NO_DATA_ERROR = 4004  # 没有检索到数据


class GetUserInfoByIDStatus:
    USER_NOT_EXISTS = 4001  # 用户不存在


class GetConnectionInfoByIDStatus:
    USERA_OR_USERB_NOT_EXISTS = 4001  # 用户不存在





#Webhome Part
class EditStatus:
    USER_NOT_EXISTS = 4001  # 用户不存在
    USER_NOT_LOGIN = 4002  # 用户未登录


#VideoManager Part
class VideoManagerStatus:
    USER_NOT_EXISTS = 4001  # 用户不存在
    USER_NOT_LOGIN = 4002  # 用户未登录
    USER_NO_POWER = 4003  # 用户权限不足


class GetVideoByIDStatus:
    VIDEO_NOT_EXISTS = 4001 # 视频不存在


class GetVideoIDNYConditionStatus:
    TYPE_ERROR = 4001  # 视频类型错误
    NO_VIDEO_EXIST = 4002  # 没有满足条件的视频

class BrowseStatus:
    VIDEO_OR_USER_NOT_EXISTS = 4001  # 视频或用户不存在

class getAuditInfoStatus:
    VIDEO_NOT_IN_AUDIT = 4001  # 视频不在审核状态
    VIDEO_NOT_EXISTS = 4002  # 视频或用户不存在
    NO_RECORD_CONCERNING = 4003  # 没有查询到相关记录

#VideoInteraction Part
class EditCommentStatus:
    COMMENT_NOT_EXISTS = 4001  # 评论不存在

class CancelCommentStatus:
    COMMENT_NOT_EXISTS = 4001  # 评论不存在
    USER_NOT_EXISTS = 4002  # 用户不存在
    VIDEO_NOT_EXISTS = 4003  # 视频不存在

class LikeStatus:
    ALREADY_LIKE = 4001  # 已经点过赞了
    USER_NOT_EXISTS = 4002  # 用户不存在
    VIDEO_NOT_EXISTS = 4003  # 视频不存在

class CancelLikeStatus:
    LIKE_NOT_EXIST = 4001  # 点赞记录不存在
    USER_NOT_EXISTS = 4002  # 用户不存在
    VIDEO_NOT_EXISTS = 4003  # 视频不存在

class FavouriteStatus:
    ALREADY_FAVOURITE = 4001  # 已经收藏了
    USER_NOT_EXISTS = 4002  # 用户不存在
    VIDEO_NOT_EXISTS = 4003  # 视频不存在

class CancelFavouriteStatus:
    FAVOURITE_NOT_EXIST = 4001  # 收藏记录不存在


class CommentStatus:
    USER_NOT_EXISTS = 4001  # 用户不存在
    VIDEO_NOT_EXISTS = 4002  # 视频不存在

class ComplaintVideoStatus:
    VIDEO_NOT_EXISTS = 4001  # 视频不存在

#UserCommunication Part


class LetterStatus:
    USER_NO_LIMIT = 4001  # 用户权限不足
    USER_NOT_EXISTS = 4002  # 发送用户或接收用户不存在

class FollowStatus:
    ALREADY_FOLLOW = 4001  # 已经关注了
    USER_NOT_EXIST = 4002  # 关注用户或被关注用户不存在

class CancelFollowStatus:
    FOLLOW_NOT_EXIST = 4001  # 关注记录不存在
    USER_NOT_EXIST = 4002  # 关注用户或被关注用户不存在