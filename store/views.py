from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from store.models import Product, Cart


class DetailView(generic.DetailView):
    model = Product
    template_name = 'store/base.html'


def home(request):
    return render(request, "store/home.html")

def checkout(request,name):
    context = {}
    return render(request, 'store/checkout.html',context)


def product(request, id):
    ls = Product.objects.filter(id=id)
    context = {'items': ls, 'image': id + '.png'}
    return render(request, 'store/product.html', context=context)

