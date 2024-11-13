from django.shortcuts import render
from .forms import AddDataUsingModelFormWithWidget

# Create your views here.


    
def showdata(request):
    return render(request, 'crud/showdata.html',{"form": AddDataUsingModelFormWithWidget})