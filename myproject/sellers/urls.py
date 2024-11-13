from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
  path('sellershome/',views.show_sellers, name="sellershome"),
]
