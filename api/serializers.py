from rest_framework import serializers
from .models import Order, OrderItem, Product, ProductImage, Review, ShippingAddress
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from cloudinary.models import CloudinaryResource

# 'image', 'metadata', 'picture', 'public_id', 'resource_type', 'signature', 'source', 'type', 'url', 'url_options', 'validate', 'version', 'video', 'video_thumbnail'

class ImageSerializer(serializers.Serializer):
    url = serializers.CharField()
    public_id = serializers.CharField()

class PhotoSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True)
    num_reviews = serializers.IntegerField(read_only=True, default=0)
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2, max_value=5, read_only=True, default=0)
    class Meta:
        model = Product
        fields = ['_id', 'title', 'price', 'brand', 'isOffer', 'discount', 'description', 'category', 'countInStock', 'images', 'slug', 'rating', 'num_reviews', 'avg_rating']


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({{"error": "Password fields didn't match."}})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Review
        fields = '__all__'


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        exclude = ['order']


class OrderItemProductSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True)
    class Meta:
        model = Product
        fields = ['_id', 'title', 'brand', 'slug', 'images']


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['_id', 'qty', 'price', 'product']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['_id', 'totalPrice', 'isPaid', 'isDelivered', 'created_at']

class OrderDetailSerializer(serializers.ModelSerializer):
    shipping = serializers.SerializerMethodField('get_shipping')
    items = serializers.SerializerMethodField('get_items')
    class Meta:
        model = Order
        exclude = ['user']
    
    def get_shipping(self, obj):
        try:
            shipping = ShippingAddress.objects.get(order=obj._id)
        except:
            raise NotFound("Something Went Wrong")
        serializer = ShippingSerializer(shipping)
        return serializer.data
    
    def get_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data