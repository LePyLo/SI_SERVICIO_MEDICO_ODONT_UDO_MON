from django.contrib import admin
from .models import User, Paciente, Doctor, Asistente, Cita, Medicamento, Recipe

# Register your models here.
admin.site.register(User)
admin.site.register(Paciente)
admin.site.register(Doctor)
admin.site.register(Asistente)
admin.site.register(Cita)
admin.site.register(Medicamento)
admin.site.register(Recipe)