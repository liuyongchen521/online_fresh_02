"""online_fresh_02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from django.contrib.staticfiles.views import serve
from .settings import MEDIA_ROOT
from django.views.static import serve
import xadmin
from rest_framework.documentation import include_docs_urls  #文档说明
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token


#viewset 和 Routers到结合使用
from goods.views import GoodsListViewSet,CategoryViewSet
from rest_framework.routers import DefaultRouter
from users.views import SmsCodeViewset,UesrViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset
from trade.views import ShoppingCartViewset,OrderViewset
router= DefaultRouter()
#配置goods的url
router.register(r'goods', GoodsListViewSet)
router.register(r"categorys",CategoryViewSet,basename="categorys")
router.register(r'code',SmsCodeViewset,basename="code")
router.register(r'users',UesrViewset,basename='users')
router.register(r'userfavs', UserFavViewset,basename="userfavs")
router.register(r'messages',LeavingMessageViewset,basename="messages")
router.register(r'address',AddressViewset,basename="address")
router.register(r'shopcarts', ShoppingCartViewset,basename="shopcarts")
router.register(r'orders',OrderViewset,basename="orders")

urlpatterns = [
    path('', include(router.urls)), #goods 的路由
    # path('favicon.ico/', serve, {'path':'favicon.ico'}),
    path('xadmin/', xadmin.site.urls),
    path("ueditor/",include("DjangoUeditor.urls")),
    #drf文档，title自定义
    path("dosc",include_docs_urls(title="王珺垚小可爱的页面")),
    path('api-auth/',include('rest_framework.urls')),  #配置第三方登录路由
    # path("goods/",include("goods.urls",namespace="goods")),  #商品APP的路由
    path("media/<path:path>", serve, {"document_root": MEDIA_ROOT}),  # 配置文件存储的路由
    # path("api-token-auth/",views.obtain_auth_token),#drf 的token
    #jwt的token认证接口
    path("login/",obtain_jwt_token),
]
