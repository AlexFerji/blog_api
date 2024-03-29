from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from blog.views import  CommentViewSet, PostViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = DefaultRouter()
router.register(r"^(?P<post_id>\d+)/comment", CommentViewSet)
router.register(r"", PostViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('v1/dj-rest-auth/', include('dj_rest_auth.urls')),
        path('v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
        ])),
    path('api/', include([
        path("v1/blog/", include(router.urls)),
    ])),
    path('api/', include([
        path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
