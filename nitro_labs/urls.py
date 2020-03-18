from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from pos import views


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
    # url(r'^auth/login/', LoginView.as_view()),
    # url(r'^auth/registration/', RegisterView.as_view()),
    # url(r'^auth/', include('rest_auth.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^api/v1/pos/(?P<p_id>[0-9]+)$', views.GetPostPOS.as_view(), name='get_post_devices'),
    # path('api/v1/pos/', views.GetPostPOS.as_view(), name='get_post_devices')
]
