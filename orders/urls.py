from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^order$', views.index, name = "list"),  # 订单页
]
