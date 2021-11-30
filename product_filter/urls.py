from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from product_filter.views import *

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='Log-In'),
    path('register/', Register.as_view(), name='User-Register'),

    
    path('jck/', JWT_ck.as_view(), name='jck'),
    path('', Product.as_view(), name='products'),
]
