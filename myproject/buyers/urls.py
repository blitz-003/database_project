from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
  path('buyerssearch/',views.search_page, name="buyerssearch"),
]
