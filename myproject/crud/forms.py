from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# class SignUpForm(UserCreationForm):
#     type = forms.CharField(max_length=20, required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'type', 'password1', 'password2', )




class AddDataUsingModelFormWithWidget(forms.ModelForm):
    # you can add extra field here and include this in the fields of Meta
    class Meta:
        model = User 
        fields = ("name","email","password")  # this follows the sequence
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        
        }



class AddDataFormUsingModelFormWithoutWidget(forms.ModelForm):
    # you can add extra field here and include this in the fields of Meta
    class Meta:
        model = User 
        fields = ("name","email","password")  # this follows the sequence
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        
        }



class AddDataUsingManualFormWithWidget(forms.ModelForm):
    # you can add extra field here and include this in the fields of Meta
    class Meta:
        model = User 
        fields = ("name","email","password")  # this follows the sequence
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        
        }


class AddDataUsingManualFormWithoutWidget(forms.ModelForm):
    # you can add extra field here and include this in the fields of Meta
    class Meta:
        model = User 
        fields = ("name","email","password")  # this follows the sequence
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        
        }
