import os

from django.shortcuts import render, redirect

from firstapp.models import Article, Comment, Ticket, UserProfile
from firstapp.forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from firstsite.settings import BASE_DIR


# Create your views here.
def index(request):
    article_list = Article.objects.all()

    page_robot = Paginator(article_list, 9)
    page_num = request.GET.get('page')
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)
        
    context = {}
    context["article_list"] = article_list

    return render(request, 'index.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    if request.method == "GET":
        form = CommentForm

    context = {}
    context["article"] = article
    context['form'] = form
    
    return render(request, 'detail.html', context)

def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]
            article = Article.objects.get(id=id)
            c = Comment(name=name, comment=comment, belong_to=article)
            c.save()
            return redirect(to="detail", id=id)
    return redirect(to="detail", id=id)

def index_login(request):
    if request.method == "GET":
        form = AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to="index")

    context = {}
    context['form'] = form

    return render(request, 'login.html', context)

def index_register(request):
    if request.method == "GET":
        form = UserCreationForm

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')

    context = {}
    context['form'] = form

    return render(request, 'register.html', context)

def vote(request, id):
    # 未登录用户不允许投票，自动跳回详情页
    if not isinstance(request.user, User):
        return redirect(to="detail", id=id)

    voter_id = request.user.id

    try:
        # 如果找不到登陆用户对此篇文章的操作，就报错
        user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=id)
        user_ticket_for_this_article.choice = request.POST["vote"]
        user_ticket_for_this_article.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id=voter_id, article_id=id, choice=request.POST["vote"])
        new_ticket.save()

    # 如果是点赞，更新点赞总数
    if request.POST["vote"] == "like":
        article = Article.objects.get(id=id)
        article.likes += 1
        article.save()

    return redirect(to="detail", id=id)

def myinfo(request):
    # 未登录用户，自动跳回登陆页
    if not isinstance(request.user, User):
        return redirect(to="login")

    if request.method == "POST":
        try:
            user = request.user
            profile = UserProfile.objects.get(id= user.belong_to.id)
            user.username = request.POST.get('name')
            profile.sex = request.POST.get('sex')
            # 存储用户上传的图片
            image = request.FILES.get('img')
            path = os.path.join(BASE_DIR, 'firstapp/media/cover_img/').replace('\\','/')
            with open(path + image.name, 'wb+')as fb:
                for chunk in image.chunks():
                    fb.write(chunk)
            profile.avatar = "/cover_img/" + image.name
            # 更新信息
            user.save()
            profile.save()
            messages.add_message(request, messages.SUCCESS, "个人信息更新成功，请刷新查看！")
            return render(request, 'myinfo.html')
        except Exception:
            messages.add_message(request, messages.ERROR, "个人信息更新失败，请重试！")
            return render(request, 'myinfo.html')

    else:
        return render(request, 'myinfo.html')

def mycollection(request):
    # 未登录用户，自动跳回登陆页
    if not isinstance(request.user, User):
        return redirect(to="login")
    ticket = Ticket.objects.filter(voter_id= request.user.id)
    # 获取用户所点赞的文章ID
    article_id = [ i.article_id for i in ticket]

    article_list = Article.objects.filter(id__in= article_id)
    # 加载分页器，分页文章
    page_robot = Paginator(article_list, 3)
    page_num = request.GET.get('page')
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)

    context = {}
    context['article_list'] = article_list

    return render(request, 'mycollection.html', context)