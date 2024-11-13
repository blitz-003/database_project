from django import forms 



class StudentRegistration(forms.Form):
    name = forms.CharField(label='My name:',help_text="Enter your name")
    email = forms.EmailField()
    first_name = forms.CharField()


class Renderfieldmanually(forms.Form):
    name = forms.CharField(label='Enter your name',help_text="Enter your name")


class Loopfield(forms.Form):
    name = forms.CharField()
    email=forms.EmailField()
    mobile=forms.IntegerField()
    key = forms.CharField(widget=forms.HiddenInput())