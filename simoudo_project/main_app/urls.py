from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_user, name="login"),
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
    path("doctores/", views.doctor_obtener_todos, name="doctores"),
    path("doctor/<int:pk>", views.doctor_detail, name="doctor_detail"),
    path("doctor/insertar", views.doctor_insertar, name="doctor_insertar"),
    path("doctor/modificar/<int:pk>", views.doctor_modificar, name="doctor_modificar"),
    path("doctor/eliminar/<int:pk>", views.doctor_eliminar, name="doctor_eliminar"),
    path("asistentes_medicos/", views.asistente_obtener_todos, name="asistentes"),
    path("asistente_medico/<int:pk>", views.asistente_detail, name="asistente_detail"),
    path("asistente_medico/insertar", views.asistente_insertar, name="asistente_insertar"),
    path("asistente_medico/modificar/<int:pk>", views.asistente_modificar, name="asistente_modificar"),
    path("asistente_medico/eliminar/<int:pk>", views.asistente_eliminar, name="asistente_eliminar"),
    path("medicamentos/", views.medicamento_obtener_todos, name="medicamentos"),
    path("medicamento/<int:pk>", views.medicamento_detail, name="medicamento_detail"),
    path("medicamento/insertar", views.medicamento_insertar, name="medicamento_insertar"),
    path("medicamento/modificar/<int:pk>", views.medicamento_modificar, name="medicamento_modificar"),
    path("medicamento/eliminar/<int:pk>", views.medicamento_eliminar, name="medicamento_eliminar"),
    
]