
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from django.conf.urls.static import static
from django.conf import settings
from django.views.defaults import page_not_found

def custom_page_not_found(request):
    return page_not_found(request, None)


handler404 = 'main_app.views.custom_404'

urlpatterns = [
    path('admin/login/', RedirectView.as_view(pattern_name='login', permanent=False)),
     path("", include("main_app.urls")),
     path('admin/', admin.site.urls),
     path('404/', custom_page_not_found),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)