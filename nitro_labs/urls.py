from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views

from main import views
from nitro_labs import settings

schema_view = get_schema_view(
    openapi.Info(
        title="NitroLabs API",
        default_version='v1',
        description="NitroLabs API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@nitro_labs.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    url('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url('^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url('^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),

    # ====== Admin ==========
    path('api/v1/admin/login/', views.AdminView.as_view(), name='token_obtain_pair'),
    path('api/v1/admin/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/admin/service/', views.ServiceView.as_view(), name='service_view'),
    path('api/v1/admin/service_log/', views.ServiceLogView.as_view(), name='service_log_view'),

    # ====== POS ==========
    path('api/v1/pos/<slug:pos_sn>', views.POSView.as_view(), name='pos_view'),

    # ====== SKU ==========
    path('api/v1/sku/pos/<slug:pos_id>', views.SKUPOSView.as_view(), name='get_sku_by_pos'),
    path('api/v1/sku/', views.SKUView.as_view(), name='sku_view'),

    # ====== Customer ======
    path('api/v1/customer/', views.CustomerView.as_view(), name='post_signup_customer'),

    # ====== Payment =======
    path('api/v1/payment/reserve/', views.PaymentReserveView.as_view(), name='reserve_payment'),
    path('api/v1/payment/check/<slug:transaction_id>', views.PaymentCheckView.as_view(), name='check_payment_status'),
    path('api/v1/payment/pay/', views.PaymentPayView.as_view(), name='pay_payment'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
