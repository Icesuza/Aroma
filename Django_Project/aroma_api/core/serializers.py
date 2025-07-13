from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

# Register Serializer

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

# Customer
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone']


# Simple Models
class ImageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageType
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDetail
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Product
class ProductSerializer(serializers.ModelSerializer):
    categoryID = CategorySerializer(read_only=True)
    categoryID_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='categoryID', write_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    productID = ProductSerializer(read_only=True)
    productID_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='productID', write_only=True)

    class Meta:
        model = ProductDetail
        fields = '__all__'

# CartItem comes first to avoid circular ref
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), source='cart', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product', 'product_id', 'quantity']

# Cart
class CartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'customer_id', 'created_at', 'items', 'total_price']

    def get_items(self, obj):
        return CartItemSerializer(obj.cartitem_set.all(), many=True).data

    def get_total_price(self, obj):
        return obj.total_price()

# QR Code
class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'

# OrderItem comes first to avoid circular ref
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='order', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product', 'product_id', 'quantity']

# Order
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'created_at', 'is_paid', 'qr_invoice', 'items', 'total_amount']

    def get_items(self, obj):
        return OrderItemSerializer(obj.orderitem_set.all(), many=True).data

    def get_total_amount(self, obj):
        return obj.total_amount()

# BlogCategory
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

# BlogDetail - REMOVE circular reference to BlogSerializer
class BlogDetailSerializer(serializers.ModelSerializer):
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), source='blog', write_only=True)

    class Meta:
        model = BlogDetail
        fields = '__all__'

# Blog
class BlogSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=BlogCategory.objects.all(), source='category', write_only=True)
    details = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_details(self, obj):
        details = BlogDetail.objects.filter(blog=obj).first()
        if details:
            return BlogDetailSerializer(details).data
        return None

# Blog Comment
class BlogCommentSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(read_only=True)
    blog_id = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), source='blog', write_only=True)

    class Meta:
        model = BlogComment
        fields = '__all__'

# Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
