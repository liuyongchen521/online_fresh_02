from rest_framework import serializers

# 用drf的序列化实现商品列表页展示
#   使用的             serializer
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()

#drf的Modelserializer实现商品列表页展示
# 上面是用Serializer实现的，需要自己手动添加字段，如果用Modelserializer，
#           会更加的方便，直接用__all__就可以全部序列化

from . models import Goods,GoodsCategory,GoodsImage

#使用的是    ModelSerializer
# category只显示分类的id，Serialzer还可以嵌套使用，覆盖外键字段

# 给分类添加三级分类的serializer
class CategorySerializer3(serializers.ModelSerializer):
    "三级分类"
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class CategorySerializer2(serializers.ModelSerializer):
    '''
    二级分类
    '''
    #在parent_category字段中定义的related_name="sub_cat"
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


#轮播图
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)

class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    #通过serializer的嵌套功能，可以详细的显示分类的信息

    #images是数据库中设置的related_name="images"，把轮播图嵌套进来
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"






