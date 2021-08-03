from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render
# Create your views here.
from common.models import Goods, Types
from common.views import loadinfo


def lists(request, page = 1):
    context = loadinfo(request)
    # 获取商品信息查询对象
    goods = Goods.objects
    #根据类型id查询
    tid = request.GET.get('tid', None)
    if tid:
        goods = goods.filter(typeid=tid)

    #关键字查询
    kw = request.GET.get('kw', None)
    if kw:
        # 过滤goods字段
        print(kw)
        goods = goods.filter(goods__icontains = kw)
        print(goods)
    goods = goods.all()

    paginator = Paginator(goods, per_page = 2)
    try:
        goods = paginator.page(page)
    except PageNotAnInteger:
        goods = paginator.page(1)
    except EmptyPage:
        goods = paginator.page(paginator.num_pages)
    except InvalidPage:
        raise Http404('找不到页面的内容')

    # # 封装信息加载模板输出
    # context['goodslist'] = goods.object_list
    # context['plist'] = paginator.page_range
    # context['page'] = page
    # context['maxpages'] = mywhere
    # context['tid'] = int(tid)
    context['goods'] = goods
    context['paginator'] = paginator
    return render(request, "goods/list.html", context=context)


def detail(request, gid):
    context = loadinfo(request)
    # 加载商品详情信息
    ob = Goods.objects.get(id = gid)
    ob.clicknum += 1
    ob.save()
    context['good'] = ob
    return render(request, "goods/detail.html", context)
