from django.shortcuts import render


# Create your views here.

def show_sellers(request):
    return render(request, 'sellers/base.html')

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello, World from sellers!')