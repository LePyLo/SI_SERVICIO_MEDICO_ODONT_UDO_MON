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
    path("cita/<int:pk>/recipe/insertar", views.recipe_insertar, name="recipe_insertar"),
    path("cita/<int:pk>/recipe", views.recipe_listar, name="recipes"),
    path("cita/recipe/modificar/<int:pk>", views.recipe_modificar, name="recipe_modificar"),
    path("pacientes/", views.paciente_obtener_todos, name="pacientes"),
    path("paciente/<int:pk>", views.paciente_detail, name="paciente_detail"),
    path("paciente/insertar", views.paciente_insertar, name="paciente_insertar"),
    path("paciente/modificar/<int:pk>", views.paciente_modificar, name="paciente_modificar"),
    path("paciente/eliminar/<int:pk>", views.paciente_eliminar, name="paciente_eliminar"),
    
]