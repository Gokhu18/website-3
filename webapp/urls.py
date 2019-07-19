from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
			url(r'^$',views.index,name='index'),	
			url(r'/logout',views.logout_view,name='logout'),
			url(r'/signup',views.signup),
			url(r'/home',views.index),
			url(r'^product_detail/(?P<id>\d+)/$',views.product_detail,name='product_details'),
			] 
