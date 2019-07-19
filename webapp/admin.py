from django.contrib import admin
from .models import product,seller,order
# Register your models here.
admin.site.register(product)
admin.site.register(seller)
admin.site.register(order)