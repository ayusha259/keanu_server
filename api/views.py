from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import OrderDetailSerializer, OrderSerializer, PhotoSerializer, ProductSerializer, ReviewSerializer, UserLoginSerializer, UserRegisterSerializer
from .models import Order, OrderItem, Product, Review, ShippingAddress, ProductImage
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Count, Avg
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

@api_view(['GET'])
def index(request):
    routes = {
        'api/products': 'Get All Products',
        'api/products/create': 'Create a product',
        'api/products/<slug:slug>': 'Get a product',
        'api/products/update/<slug:slug>': 'Update a product',
        'api/prodcuts/delete/<slug:slug>': 'Delete a prodcuct'
    }
    return Response(routes)


@api_view(['GET'])
def get_all_products(request):
    paginator = PageNumberPagination()
    paginator.page_size = 9
    
    sort_by = request.GET.get('sort', '-avg_rating')

    categories = request.GET.get("categories", "")
    brands = request.GET.get("brands", "")
    categories = categories.split(",") if (len(categories) > 0) else []
    brands = brands.split(",") if (len(brands) > 0) else []

    if (len(categories) > 0) and (len(brands) > 0):
        data = Product.objects.filter(Q(category__in = categories) & Q(brand__in = brands))
    elif (len(categories) > 0 and (len(brands) == 0)):
        data = Product.objects.filter(category__in = categories)
    elif (len(brands) > 0 and (len(categories) == 0)):
        data = Product.objects.filter(brand__in = brands)
    else:
        data = Product.objects.all()
    data = data.annotate(num_reviews=Count('reviews')).annotate(avg_rating = Avg('reviews__rating')).order_by(sort_by)
    data = paginator.paginate_queryset(data, request)
    serializer = ProductSerializer(data, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.annotate(num_reviews=Count('reviews')).annotate(avg_rating = Avg('reviews__rating')).get(slug = pk)
        serializer = ProductSerializer(product)
    except IndexError:
        raise Http404()
    return Response({'product': serializer.data})


@api_view(['GET'])
def temp_view(request):
    product = Product.objects.get(_id=11)
    serializer = ProductSerializer(product)
    return Response({'product': serializer.data})

@api_view(['GET'])
def get_options(request):
    brands = Product.objects.all().values("brand").distinct()
    categories = Product.objects.all().values("category").distinct()
    list_brands = [b['brand'] for b in brands]
    list_categories = [c['category'] for c in categories]
    response = {
        'brands': list_brands,
        'categories': list_categories
    }
    return Response(response)

@api_view(['POST'])
def user_signup(request):
    data = request.data
    serializer = UserRegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "User Created"})
    
@api_view(['POST'])
def user_login(request):
    data = request.data
    seriallizer = UserLoginSerializer(data=data)
    seriallizer.is_valid(raise_exception=True)
    response = {
        'token': seriallizer.data['token']
    }
    return Response(response)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    serializer = UserLoginSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
def get_product_reviews(request, pk):
    paginator = PageNumberPagination()
    paginator.page_size = 4

    sort_by = request.GET.get('sort', '-rating')

    reviews = Review.objects.filter(product___id=pk).order_by(sort_by)
    data = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(data, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_product_review(request):
    user = request.user
    data = request.data
    data['user'] = user
    serializer = ReviewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_a_order(request):
    user = request.user
    data = request.data


    order = data['order']
    order['user'] = user
    order = Order(**order)
    order.save()
    
    shipping = data['shipping']
    shipping['order'] = order

    shipping = ShippingAddress(**shipping)
    shipping.save()

    items = data['items']
    for o in items:
        product = get_object_or_404(Product, _id=o['_id'])
        OrderItem.objects.create(order=order, product=product, qty=o['qty'], price=o['price'])
        product.countInStock -= int(o['qty'])
        product.save()
    
    return Response({"detail": "Success"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    serilizer = OrderSerializer(orders, many=True)
    return Response(serilizer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        if order.user != user:
            raise NotAuthenticated("You are not authenticated")
    except:
        raise Http404()
    serializer = OrderDetailSerializer(order)
    return Response(serializer.data)

@api_view(['GET'])
def getImages(request):
    photos = ProductImage.objects.all()
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data)