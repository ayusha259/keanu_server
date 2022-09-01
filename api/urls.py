from django.urls import path
from . import views
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token
    
    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        try:
            User.objects.get(username=username)
        except:
            raise AuthenticationFailed("No user exist with the given username")
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Password is incorrect")    
        
        return super().validate(attrs)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('', views.index, name='index'),

    path('users/login', MyTokenObtainPairView.as_view(), name='user_login'),

    path('users/signup', views.user_signup, name="create_user"),

    path('users/user', views.user_details, name="get_user"),

    path('orders', views.get_all_orders, name='get_all_orders'),

    path('orders/place', views.place_a_order, name='place_a_order'),

    path('orders/<int:pk>', views.get_order_by_id, name='get_order_by_id'),

    path('products', views.get_all_products, name='get_all_products'),

    path('products/get_options', views.get_options, name="get_options"),

    path('products/temp_view', views.temp_view, name='temp'),

    path('products/<slug:pk>', views.get_product, name='get_product'),

    path('reviews', views.post_product_review, name='post_review'),

    path('reviews/<int:pk>', views.get_product_reviews, name='get_product_reviews'),

    path("test", views.getImages)
]