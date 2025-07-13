from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'image-types', ImageTypeViewSet, basename='imagetype')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'menu-details', MenuDetailViewSet, basename='menudetail')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-details', ProductDetailViewSet, basename='productdetail')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'qrcodes', QRCodeViewSet, basename='qrcode')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'blog-categories', BlogCategoryViewSet, basename='blogcategory')
router.register(r'blog-details', BlogDetailViewSet, basename='blogdetail')
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'blog-comments', BlogCommentViewSet, basename='blogcomment')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
urlpatterns = [
    path('', include(router.urls)),
]
