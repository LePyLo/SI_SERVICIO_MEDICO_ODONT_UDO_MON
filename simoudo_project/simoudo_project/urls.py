
from django.contrib import admin
from django.urls import include, path

handler404 = 'main_app.views.custom_404'

urlpatterns = [
     path("sis/", include("main_app.urls")),
    path('admin/', admin.site.urls),
]
