"""
枚举类：定义状态码，用于前后端传输
"""

SUCCESS = '0'
DEFAULT = '2001'  # 没发送请求或发送请求类型不对
FORM_ERROR = '3001'  # 表单信息错误（未全部填写或数据类型有误）

# 系统错误
PAGE_NOT_FOUND = '404'


# Wrong

#Weblogin Part
class LoginStatus:  #WebLogin.login
    LOGIN_REPEATED = '4001'  # 用户已登录
    EMAIL_MISS = '4002'  # 邮箱不存在
    PASSWORD_ERROR = '4003'  # 密码错误
    USER_NOT_CONFIRM = '4004'  # 用户未通过邮件验证



class RegisterStatus:  #Weblogin.register
    USERNAME_REPEATED = '4001'  # 用户名已存在
    EMAIL_ERROR = '4002'  # 邮箱已存在
    PASSWORD_INVALID = '4003'  # 密码不符合规则，应至少同时包含字母和数字，且长度为 8-18
    PASSWORD_CONTRAST = '4004'  # 两次输入的密码不同
    SEND_EMAIL_ERROR = '4005'  # 邮件验证码发送失败


class LogoutStatus:   #Weblogin.logout
    USER_NOT_LOGIN = '4001'  # 用户未登录


class ConfirmStatus:  #Weblogin.user_confirm
    STRING_MISS = '4001'  # 验证码不存在，即返回无效的确认请求
    CONFIRM_EXPIRED = '4002'  # 验证码已过期，请重新注册


class ForgetPasswordStatus:   #Weblogin.forget_pwd
    SEND_EMAIL_ERROR = '4001' #邮件发送失败
    EMAIL_MISS = '4002' #邮箱还未注册


class PasswordUpdateStatus:   #Weblogin.update_pwd
    PASSWORD_INVALID = '4001' #密码不符合规范
    STRING_ERROR = '4002' #验证码错误


#Websurf Part



#Webhome Part



#VideoManager Part



#VideoInteraction Part



#UserCommunication Part