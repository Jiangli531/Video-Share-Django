from django import forms

class DetailInfoForm(forms.Form):
    username = forms.CharField(max_length=128, label='用户名')
    userInformation = forms.CharField(max_length=500, label='个人简介')
    userSex = forms.CharField(max_length=32, label='性别')
    userBirthday = forms.DateField(label='生日')