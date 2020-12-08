from django.shortcuts import render
from django.views.generic import View
from goods.models import Goods
from django.http import HttpResponse,JsonResponse
import json

# 为了引入django rest framework和简单介绍django的序列化用法↓

# class GoodsListView(View):
#     def get(self,request):
#         #通过django的view实现商品列表页
#         json_list = []
#         #获取所有商品
#         goods = Goods.objects.all()
#
#         #1、将数据库转换为字典 ，便于序列化
#         # for good in goods:
#         #     json_dict = {}
#         #     #获取商品的每个字段，键值对形式
#         #     json_dict['name'] = good.name
#         #     json_dict['category'] = good.category.name
#         #     json_dict['market_price'] = good.market_price
#         #     json_list.append(json_dict)
#
# #       2、 当字段比较多时，一个字段一个字段的提取很麻烦，
#         #        可以用model_to_dict，将model整个转化为dict
#         # from django.forms.models import model_to_dict
#         # for good in goods:
#         #     json_dict = model_to_dict(good)
#         #     json_list.append(json_dict) #但是这样有个问题，
#                                 # 就是ImageFieldFile 和add_time字段不能序列化
#
#         #3、如何才能将所有字段序列化呢？就要用到django的serializers序列化器
#         from django.core import serializers
#         json_data = serializers.serialize("json",goods)
#         json_data = json.loads(json_data)
#         #
#         #返回json，一定要指定类型content_type='application/json'
#         # return HttpResponse(json.dumps(json_list),content_type='application/json')
#         # return JsonResponse(json_list,content_type="application/json",safe=False)
#         return JsonResponse(json_data,content_type="application/json",safe=False)
#django的serializer虽然可以很简单实现序列化，但是有几个缺点
        #字段序列化定死的，要想重组的话非常麻烦
        #从上面截图可以看出来，images保存的是一个相对路径，
#               我们还需要补全路径，而这些drf都可以帮助我们做到
#以上写了这么多只是为了引入django rest framework和简单介绍django的序列化用法，
# 下面就是重点讲解django rest framework了
# pip install coreapi                         drf的文档支持
# pip install django-guardian           drf对象级别的权限支持

from rest_framework.views import APIView
# from goods.serializers import GoodsSerializer
# from .models import Goods
from rest_framework.response import Response
from rest_framework.views import status


"""使用APIview """

# class GoodsListView(APIView):
#     '''
#     商品列表
#     '''
#     def get(self,request,format=None):
#         goods = Goods.objects.all()
#         goods_serialzer = GoodsSerializer(instance=goods,many=True)
#         return Response(goods_serialzer.data,status=status.HTTP_200_OK)



""" GenericView实现商品列表页"""

# GenericAPIView继承APIView，封装了很多方法，比APIView功能更强大
# 用的时候需要定义queryset和serializer_class
# GenericAPIView里面默认为空
# queryset = None
# serializer_class = None
# ListModelMixin里面list方法帮我们做好了分页和序列化的工作，只要调用就好了

# from rest_framework import mixins
# from rest_framework import generics
# from rest_framework.pagination import PageNumberPagination
# 自定义分页功能
# class GoodsPagination(PageNumberPagination):
#     """
#     商品列表自定义分页
#     """
#     #默认每页显示的个数
#     page_size = 10
#     #可以动态改变每页显示的个数
#     page_size_query_param =  'page_size'
#     #页码参数
#     page_query_param = 'page'
#     #最多显示多少页
#     max_page_size = 10

# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     """
#     商品列表页
#     """
#     pagination_class = GoodsPagination  #分页
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

""" viewsets和router完成商品列表页
    主要用到viewsets中的GenericViewSet
 """
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination# 分页
from django_filters.rest_framework import DjangoFilterBackend #过滤器后端
from . filters import GoodsFilter  #自定义的过滤器类
from rest_framework import filters
from goods.serializers import GoodsSerializer,CategorySerializer
from .models import Goods,GoodsCategory

# 自定义分页功能
class GoodsPagination(PageNumberPagination):
    """
    商品列表自定义分页
    """
    #默认每页显示的个数
    page_size = 10
    #可以动态改变每页显示的个数
    page_size_query_param =  'page_size'
    #页码参数
    page_query_param = 'page'
    #最多显示多少页
    max_page_size = 100

class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    '商品列表页'

    # 分页
    pagination_class = GoodsPagination
    #这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer #序列化的类

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    #设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # drf的搜索和排序
    #搜索的字段可以使用正则表达式，更加的灵活
    search_fields = ("name",'goods_brief','goods_desc')
    # 添加排序功能
    ordering_fields = ("sold_num","shop_price")



#分类的显示
class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        商品分类列表展示
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer



#
# 5.8.drf的APIView、GenericView、viewsets和router的原理分析
# genericViewSet
# 是最高的一层
# 往下
# GenericViewSet（viewsets）     ----drf
# 　　GenericAPIView - --drf
# 　　　　APIView - --drf
# 　　　　　　View　　　　        ----django
# 这些view功能的不同，主要的是有mixin的存在
# mixins总共有五种：
# 　　CreateModelMixin  添加
# 　　ListModelMixin    展示
# 　　UpdateModelMixin   更新
# 　　RetrieveModelMixin  详情
# 　　DestoryModelMixin