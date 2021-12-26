from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .router import router

admin.site.site_header = getattr(settings, 'PROJECT_NAME_HEADER')
admin.site.site_title = getattr(settings, 'PROJECT_NAME_TITLE')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
