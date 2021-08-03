from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.urls import reverse
from common.models import User


def index(request):
    return HttpResponse("首页")


def login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    else:
        try:
            username = request.POST['username']
            password = request.POST['password']
            print(request.POST)
            print(request.POST['username'])
            user = User.objects.get(username = username)
            if user.state == 0 or user.state == 1:
                if user.password == password:
                    request.session['vipuser'] = user.toDict()
                    print('ok')
                    return redirect(reverse('index'))
                else:
                    context = {'info': '登录密码错误!'}
                    print(context)
            else:
                context = {'info': '此用户为非法用户!'}
                print('context')
        except:
            context = {'info': '登录账号错误!'}
            print(context)
    return render(request, "users/login.html", context)


def logout(request):
    del request.session['vipuser']
    return redirect(reverse('login'))


def register(request):
    return HttpResponse("注册")
