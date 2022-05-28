from Weblogin.models import UserInfo

from django import forms


# 登录表单
class LoginForm(forms.Form):
    email = forms.EmailField(label="个人邮箱", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=128,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="个人邮箱", widget=forms.EmailInput(attrs={'class': 'form-control'}))


# 忘记密码表单
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label='注册邮箱地址', min_length=4, widget=forms.EmailInput(attrs={'class': 'form-control'}))
