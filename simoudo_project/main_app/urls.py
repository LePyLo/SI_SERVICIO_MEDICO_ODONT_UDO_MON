from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/",views.logout_user, name="logout"),
    path("cita/<int:pk>", views.cita_detail, name="cita_detail"),
    path("citas/", views.cita_obtener_todas, name="citas"),
    path("cita/insertar", views.cita_insertar, name="cita_insertar"),
    path("cita/modificar/<int:pk>", views.cita_modificar, name="cita_modificar"),
    path("cita/eliminar/<int:pk>", views.cita_eliminar, name="cita_eliminar"),
    path("cita/<int:pk>/medicamento/insertar", views.recipe_insertar, name="recipe_insertar"),
    path("cita/<int:pk>/medicamentos", views.recipe_listar, name="recipes"),
    
]