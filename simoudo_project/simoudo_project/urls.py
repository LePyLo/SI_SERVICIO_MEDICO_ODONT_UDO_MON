
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

handler404 = 'main_app.views.custom_404'

urlpatterns = [
    path('admin/login/', RedirectView.as_view(pattern_name='login', permanent=False)),
     path("", include("main_app.urls")),
     path('admin/', admin.site.urls),
    
]
