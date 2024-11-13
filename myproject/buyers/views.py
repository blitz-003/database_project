
# Create your views here.
from django.shortcuts import render


# Create your views here.

def search_page(request):
    return render(request, 'buyers/search.html')

def product_list(request):
    return render(request, 'buyers/productlist.html')

def individual_product(request):
    return render(request, 'buyers/individualproduct.html')

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello, World from sellers!')