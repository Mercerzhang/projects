# 从urls模块中导入url
from django.conf.urls import url


# 从当前目录导入我们的视图模块views
from . import views

urlpatterns = [
    # 商品列表页
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view(), name='list'),

    # 热销商品排行
    url(r'^hot/(?P<category_id>\d+)/$', views.HotGoodsView.as_view()),
    # 商品详情页
    url(r'^detail/(?P<sku_id>\d+)/$', views.DetailView.as_view(), name='detail'),
    # 记录详情页的访问量
    url(r'^detail/visit/(?P<category_id>\d+)/$', views.DetailVisitView.as_view()),

]
