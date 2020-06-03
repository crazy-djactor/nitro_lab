from main.models import Discount, POS, SKU, Service, OrderLog, Transaction, ServiceLog, \
    LocationProduct, Customer, Promo, Matching
from django.contrib import admin


admin.site.register(POS)
admin.site.register(SKU)
admin.site.register(Discount)
admin.site.register(OrderLog)
admin.site.register(Service)
admin.site.register(ServiceLog)
admin.site.register(Transaction)
admin.site.register(LocationProduct)
admin.site.register(Customer)
admin.site.register(Promo)
admin.site.register(Matching)
