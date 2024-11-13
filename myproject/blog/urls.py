from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
  path('',views.home, name="home"),
   path('test/',views.test, name="blog_test"),
   path('about/',views.about, name="about"),
   path('contact/',views.contact, name="contact"),
   path('dashboard/',views.dashboard, name="dashboard"),
   path('signup/',views.signup, name="signup"),
   path('userlogin/',views.userlogin, name="userlogin"),
   path('logoutview/',views.logoutview, name="logoutview"),
   #buyer
   path('buyerprofile/<int:id>',views.buyerprofile, name="buyerprofile"),
  path('buyerupload/',views.buyerupload, name="buyerupload"), 
  path('buyersearch/',views.buyersearch, name="buyersearch"),
  path('buyerproductdetail/<int:id>',views.buyerproductdetail, name="buyerproductdetail"),
  path('buyerproductdetailpricehistory/<int:id>',views.buyerproductdetailpricehistory, name="buyerproductdetailpricehistory"),
  path('buyermessagelist/<int:id>',views.buyermessagelist, name="buyermessagelist"),
  path('buyerbookmarklist/',views.buyerbookmarklist, name="buyerbookmarklist"),
  # path('buyersearchresult/',views.buyersearchresult, name="buyersearchresult"), 
  #seller
  path('sellerprofile/<int:id>',views.sellerprofile, name="sellerprofile"),
  path('sellerupload/',views.sellerupload, name="sellerupload"), 
  path('sellerproductlist/',views.sellerproductlist, name="sellerproductlist"),
  path('sellerproductdetail/<int:id>',views.sellerproductdetail, name="sellerproductdetail"),
  path('sellerproductdetailupdate/<int:id>',views.sellerproductdetailupdate, name="sellerproductdetailupdate"),
  #admin
  path('adminprofile/',views.adminprofile, name="adminprofile"),
  path('adminlistofbuyers/',views.adminlistofbuyers, name="adminlistofbuyers"), 
  path('adminlistofsellers/',views.adminlistofsellers, name="adminlistofsellers"),
  path('adminproductlist/',views.adminproductlist, name="adminproductlist"),
  path('adminproductdetail/<int:id>',views.adminproductdetail, name="adminproductdetail"),
  path('adminproductdetailupdate/<int:id>',views.adminproductdetailupdate, name="adminproductdetailupdate"),
  path('adminproductdetailpricehistoryupdate/<int:id>',views.adminproductdetailpricehistoryupdate, name="adminproductdetailpricehistoryupdate"),
  path('admininsights/',views.admininsights, name="admininsights"),
  path('adminspdmpd/',views.adminspdmpd, name="adminspdmpd"),
  path('groupby/',views.groupby, name="groupby"),
  #path('groupbydetail/',views.groupbydetail, name="groupbydetail"),

  #ajaxpost
  path('ajaxpostforpricealert/',views.ajaxpostforpricealert, name="ajaxpostforpricealert"), 
  path('ajaxpostforbookmarklist/',views.ajaxpostforbookmarklist, name="ajaxpostforbookmarklist"), 


]
