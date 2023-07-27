from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *


@login_required
def market(request):
    products = Product.objects.all()
    unavailableProducts = []
    countBuyProducts = {}
    balance = request.user.score

    for product in products:
        if product.price > balance:
            unavailableProducts.append(product.id)

        try:
            buyProductsQuery = Order.objects.filter(user=request.user, product=product)
            countBuyProducts[product.id] = len(buyProductsQuery)
        except Order.DoesNotExist:
            countBuyProducts[product.id] = 0

    navbars = [
        {
            'url': 'personal',
            'title': request.user.first_name,
            'is_active': False
        },
        {
            'url': 'timetable',
            'title': 'Расписание',
            'is_active': False
        },
        {
            'url': 'market',
            'title': 'Магазин',
            'is_active': True
        },
    ]

    return render(request, 'market.html', context={
        'navbars': navbars,
        'products': products,
        'unavailableProducts': unavailableProducts,
        'countBuyProducts': countBuyProducts
    })

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required
def buyProducts(request, pk):
    product = Product.objects.get(pk=pk)
    Order.createOrder(request.user, product)
    
    return HttpResponseRedirect(reverse('market'))