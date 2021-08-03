from json import dumps

from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
# 公共信息加载
from django.urls import reverse
from common.models import Types, Goods
from common.views import loadinfo


def index(request):
    '''浏览购物车'''
    context = loadinfo(request)
    if 'shoplist' not in request.session:  # 会话中没有shoplist购物车
        request.session['shoplist'] = {}
    context['shoplist'] = request.session['shoplist']
    return render(request, "cart/cart.html", context)


def add(request, gid):
    '''在购物车中放入商品信息'''
    # 获取要放入购物车中的商品信息
    goods = Goods.objects.get(id = gid)
    print(goods)
    shop = goods.toDict()
    shop['m'] = int(request.POST.get('m', 1))  # 添加一个购买量属性m
    # 从session获取购物车信息，没有默认空字典
    shoplist = request.session.get('shoplist', {})
    # print('shoplist', shoplist)
    # 判断此商品是否在购物车中
    if gid in shoplist:
        # 商品数量加
        shoplist[gid]['m'] += shop['m']
    else:
        # print('shop:',type(shop))
        # print('shoplist:', type(shoplist))
        # print('gid', type(gid))
        # 新商品添加
        # shoplist['111'] = shop
        shoplist[gid] = shop
        # print(shoplist)
        # 将购物车信息放回到session
    request.session['shoplist'] = shoplist
    # 重定向到浏览购物车页
    return redirect(reverse('cart_index'))
    # return render(request,"cart/cart.html")


def delete(request, gid):
    '''删除一个商品'''
    shoplist = request.session['shoplist']
    del shoplist[gid]
    request.session['shoplist'] = shoplist
    return redirect(reverse('cart_index'))


def clear(request):
    '''清空购物车'''
    context = loadinfo(request)
    request.session['shoplist'] = {}
    return redirect(reverse('cart_index'))
    # return render(request,"cart/cart.html",context)


def change(request):
    '''更改购物车中的商品信息'''
    # context = loadinfo(request)
    shoplist = request.session['shoplist']
    # 获取信息
    shopid = request.GET.get('gid', '0')
    num = int(request.GET['num'])
    if num < 1:
        num = 1
    shoplist[shopid]['m'] = num  # 更改商品数量
    request.session['shoplist'] = shoplist
    return redirect(reverse('cart_index'))


def pay(request):
    orderlist = request.session['shoplist']
    context = loadinfo(request)
    context['orderlist'] = orderlist
    print(type(orderlist))
    total_price = 0.0
    for item in orderlist.values():
        total_price += item['m'] * item['price']
    context['total_price'] = total_price
    return render(request, "orders/order.html", context)

