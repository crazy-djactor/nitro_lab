from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views

from main import views

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
    path('admin/', admin.site.urls),

    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('profile/admin', views.GetProfile.as_view(), name='get_user'),
    path('profile/user/', views.GetProfile.as_view(), name='get_user'),
    path('profile/user/register', views.CreateUserProfile.as_view(), name='create_user'),

    url('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url('^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url('^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/pos/list/', views.GetPOSList.as_view(), name='get_pos_list'),
    path('api/v1/pos/new_pos/', views.PostPOS.as_view(), name='post_pos'),
    path('api/v1/pos/<slug:p_id>', views.GetPutPatchDeletePOS.as_view(), name='get_post_devices'),

    path('api/v1/sku/list/', views.GetSKUList.as_view(), name='get_sku_list'),
    path('api/v1/sku/new_sku/', views.PostSKU.as_view(), name='post_sku'),
    path('api/v1/sku/<slug:s_id>/', views.GetPutPatchDeleteSKU.as_view(), name='get_sku'),
]
