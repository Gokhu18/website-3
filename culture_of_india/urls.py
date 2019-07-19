"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from webapp.views import p1,index,logout_view,signup,product_detail,review_now,orders,checkout,add_to_cart,cart1,sell,order1,remove_cart
from webapp.views import cart_update
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
 	url(r'^auth/', include('social_django.urls', namespace='social')),
 	url(r'^product/(?P<id>\d+)/$',product_detail,name='product_details'),
 	url(r'^cart_update/(?P<id>\d+)/$',cart_update,name='cart_update'),
 	url(r'^add_to_cart/product/(?P<id>\d+)/$',add_to_cart,name='add_to_cart'),
 	url(r'^review/product/(?P<id>\d+)/$',review_now,name='review'),
 	url(r'^cart/',cart1,name='cart'),
 	url(r'^Checkout/',checkout,name='cart'),
 	url(r'^product1/(?P<id>\d+)/$',p1,name='p1'),
 	url(r'^books/',checkout,name='cart'),
 	url(r'^miscellaneous/',checkout,name='cart'),
 	url(r'^order/',order1,name='order'),
 	url(r'^remove_cart/(?P<id>\d+)',remove_cart,name='remove_cart'),
 	url(r'^sell/',sell,name='sell'),
 	url(r'^$',index,name='home'),
 	url(r'^logout',logout_view,name='logout'),
 	url(r'^signup',signup),
 	url(r'^imagefit/', include('imagefit.urls')),
    url(r'^$',include('webapp.urls')),
    url(r'^orders/',orders,name='orders')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
