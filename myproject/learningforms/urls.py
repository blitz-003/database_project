from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
  path('',views.showformdata, name="showformdata"),
path('renderfieldmanually/',views.renderfieldmanually, name="renderfieldmanually"),
path('loopfield/',views.loopfield, name="loopfield"),

]
