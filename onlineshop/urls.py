from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
import debug_toolbar
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),

    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('customers.urls')),
    path('api/v1/', include('product_social_media.urls')),  # SHOULD BE IN TOP OF PRODUCT URLS
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('shopcarts.urls')),
    path('api/v1/', include('social_media.urls')),
    # path('api/v1/',include('')),
]\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
