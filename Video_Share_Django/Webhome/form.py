from django import forms

class DetailInfoForm(forms.Form):
    userID = forms.IntegerField(label='用户id')
    username = forms.CharField(max_length=500, label='用户昵称')
    userInformation = forms.CharField(max_length=500, label='个人简介')
    userSex = forms.CharField(max_length=32, label='性别')
    userBirthday = forms.DateField(label='生日')