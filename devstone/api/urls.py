from django.urls import path,include
from . import views
from .products.views import getProductDetailList

urlpatterns = [
    path('collections/',include('api.collections.urls')),
    path('allproductdetail/', getProductDetailList.as_view() , name='product detail'),
    path('account/', include('api.account.urls')),
    path('carts/',include('api.carts.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
