from django.shortcuts import render
from django.contrib.auth.models import User


# 手机端页面的视图函数皆在于此，分类处理，与view分隔开

def video_list(request):
    return render(request, 'mobile_list.html', {})

# 在这里只返回网页，数据由对应的API接口获取
def user_list(request):
    return render(request, 'userListPanel.html', {})

# 移动端登录页面
def mobile_login(request):
    return render(request, 'userListPanelLogin.html', {})

# 用户信息表页面
def user_detail(request, id):
    context = {}
    context['id'] = id
    user_pic = User.objects.get(id=id).profile.profile_image
    context['userpic'] = user_pic

    return render(request, 'userDetail.html', context)
