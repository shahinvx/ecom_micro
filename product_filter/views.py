from functools import reduce
from django.conf.urls import url
from django.http.request import HttpHeaders
from numpy.core.numeric import NaN
import pandas as pd
# from typing_extensions import final
from django.core import paginator
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from numpy.lib.stride_tricks import _broadcast_shape
from requests.api import head
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db.models.expressions import Value
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import fields, generics, serializers
from rest_framework import status
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator
from .models import *
import requests
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt import authentication
from django.contrib.auth import authenticate
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

store = []
price_range = [0, 20000]


class Home(APIView):
    # @method_decorator(login_required(login_url='login'), name='dispatch')
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        store.clear()
        return redirect('products')

# class Login(APIView):
#     def get(self, request, format=None):
#         return render(request=request, template_name="login.html", )#context=context

class Register(APIView):
    def get(self, request, format=None):
        # context=context
        return render(request=request, template_name="register.html", )

class JWT_ck(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('--------------------auth JWT : ', request.user)
        data = {'user': str(request.user)}
        return Response(data)

# http://127.0.0.1:8000/login/


class Login(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'home_product.html'
    # def get(self, request, format=None):
    #     return render(request=request, template_name="login.html", )

    def post(self, request, format=None):
        print('------------------------------------->User login ',
              request, request.POST)
        user_name = request.data.get("username")
        user_pass = request.data.get("password")

        print('------------------------------------->User login ',
              user_name, user_pass)

        # user = authenticate(request, username=username, password=password)

        # if user is not None:
        # 	login(request, user)
        # 	return redirect('home')
        # else:
        # 	messages.info(request, 'Username OR password is incorrect')

        # {"username":"shahinvx","password":"shahin"}
        # pload = {'username': user_name, 'password': user_pass} json.loads(data.text)
        # data = requests.post('http://127.0.0.1:8000/api/token/', data=pload)
        # user = authenticate(request, username=user_name, password=user_name)
        user = User.objects.get(username=user_name)
        refresh = RefreshToken.for_user(user)
        refresh_response = {'refresh': str(
            refresh), 'access': str(refresh.access_token), }

        # print('---------------------------------- JWT > ',json.loads(data.text), type(data.text))
        headers = {'Authorization': 'Bearer '+refresh_response['access']}

        print('---------------------------------- JWT Refresh > ', headers)

        # return Response(refresh_response)

        # response = redirect('jck')
        # response['headers'] =  refresh_response['access']
        # response['WWW-Authenticate'] =  refresh_response['access']
        # response['Token'] =  refresh_response['access']
        # return response

        request.headers = refresh_response['refresh']
        return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/jck/', requests=request)

        # Working
        # return Response(template_name='home_product.html', headers=headers)

        # response = redirect('http://127.0.0.1:8000/')
        # response['headers'] =  headers #refresh_response['refresh']
        # response['WWW-Authenticate'] =  headers
        # response['Bearer'] =  headers
        # return response

        # request.headers = refresh_response['refresh']
        # return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/', requests=request)

        # request.headers = refresh_response['refresh'] # Working
        # return render(request=request,template_name='home_product.html') # Working

        # return redirect('products',headers=headers) # Working
        # return Response(refresh_response)
        # return requests(request=request, HttpHeaders=refresh_response, url='http://127.0.0.1:8000/')
        # return Response(headers=refresh_response,template_name='home_product.html')
        # return redirect('products')  # HttpHeaders=refresh_response,user_name=
        # return render(HttpHeaders=refresh_response,request=request, template_name="home_product.html", )


class Product(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if store:
            product = FinalAmazonV2.objects.filter(
                category__contains=store[-1])
        else:
            product = FinalAmazonV2.objects.all()

        if request.GET.get('delivery'):
            product = product.filter(
                shiping__contains=request.GET.get('delivery'))

            print('Request : ', request.GET.get('delivery'), product.count())

        if request.GET.get('p_range') or (request.GET.get('min_val') and request.GET.get('max_val')):
            try:
                price_range[0] = int(request.GET.get(
                    'p_range').split(',')[0])  # min
                price_range[1] = int(request.GET.get(
                    'p_range').split(',')[1])  # max
            except:
                a = 0
            if (request.GET.get('min_val') and request.GET.get('max_val')):
                price_range[0] = int(request.GET.get('min_val'))
                price_range[1] = int(request.GET.get('max_val'))

            product = product.filter(
                selling_price__lte=price_range[1], selling_price__gte=price_range[0])
            if product.count() == 0:
                price_range[0] = 0
                price_range[1] = 20000
                product = product.filter(
                    selling_price__lte=price_range[1], selling_price__gte=price_range[0])
        else:
            product = product.filter(
                selling_price__lte=price_range[1], selling_price__gte=price_range[0])

        paginator = Paginator(product, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        my_cat_list = []
        shiping_option = set()
        for i in product:
            categry = i.category
            if i.shiping != '0' and i.shiping != '1':
                shiping_option.add(i.shiping)
            try:
                my_cat_list.extend(categry.split('|'))
            except:
                a = 0

        final_category = []
        for cat in pd.Series(my_cat_list).value_counts().iloc[:5].index:
            cat = cat.lstrip()
            cat = cat.rstrip()
            final_category.append(cat)
        print(final_category)

        product_type = request.GET.getlist('type_p')
        print('------------------------------------- > All Filter Params : ',
              product_type, page_number, request.get_full_path, store)
        try:
            print('-----------------------> ',
                  final_category[int(product_type[0])-1], product_type)
            product_type = str(final_category[int(product_type[0])-1])
            print('----------------------------------- > Filter', product_type)
            # data = FinalAmazonV2.objects.get(category__iexact=product_type)
            product = FinalAmazonV2.objects.filter(
                category__contains=product_type)
            shiping_option = dict.fromkeys(shiping_option)
            shiping_option['Conditional Delivery'] = [product.filter(
                shiping__contains='Conditional Delivery').count()]
            shiping_option['Free Delivery'] = [product.filter(
                shiping__contains='Free Delivery').count()]

            paginator = Paginator(product, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            store.append(product_type)
        except:
            shiping_option = dict.fromkeys(shiping_option)
            shiping_option['Conditional Delivery'] = [product.filter(
                shiping__contains='Conditional Delivery').count()]
            shiping_option['Free Delivery'] = [product.filter(
                shiping__contains='Free Delivery').count()]

        bread_li = []
        try:
            bread_li.append(store[-1])
        except:
            bread_li = []

        if request.GET.get('delivery'):
            shiping_option[request.GET.get('delivery')].append('true')

        print(len(my_cat_list), len(list(set(my_cat_list))),
              'Shiping : ', shiping_option)
        context = {'product': page_obj, 'total_product': product.count(
        ), 'filter_category': final_category, 'bread': bread_li, 'shiping': shiping_option, 'price_range': price_range}
        return render(request=request, template_name="home_product.html", context=context)
