from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

from .forms import StudentRegistration, Renderfieldmanually, Loopfield


#
def showformdata(request):
    fm = StudentRegistration(auto_id=True,  label_suffix='', initial={'name': 'Sonam'})

    fm.order_fields(field_order=['email', 'first_name', 'name'])

    return render(request, 'learningforms/learningforms.html', {"form": fm})


def renderfieldmanually(request):
    fm = Renderfieldmanually(auto_id=True, initial={'name': 'Sonam'})

    

    return render(request, 'learningforms/renderfieldmanually.html', {"form": fm})



def loopfield(request):
    fm = Loopfield(auto_id=True, initial={'name': 'Sonam'})

    return render(request, 'learningforms/loopfield.html', {"form": fm})


def userlogin(request):
    if request.method == "POST":
        print("userlogin post")
        fm = AuthenticationForm(request = request, data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data["username"]
            password = fm.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                if user.profile.type == "buyer":
                    return redirect('buyerprofile',id=request.user.id)
                elif user.profile.type == "seller":
                    return redirect('sellerprofile', id = request.user.id)
                elif user.profile.type == "admin":
                    return redirect('adminprofile', id = request.user.id)
            else:
                print("user not found")
                fm = AuthenticationForm()
                return render(request, 'blog/userlogin.html', {"form": fm})   

    else:
        fm = AuthenticationForm()
        return render(request, 'blog/userlogin.html', {"form": fm})

        
    return render(request, 'blog/userlogin.html')

