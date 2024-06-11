from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from .models import Cita, Medicamento, Doctor, Asistente, Recipe, Paciente
from django.utils import timezone
import re


class CitaForm(forms.ModelForm):
    

   # Personalizar etiquetas
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), label='Paciente', widget=forms.Select(attrs={'class': 'form-control'}))
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label='Doctor', widget=forms.Select(attrs={'class': 'form-control'}))
    asistente = forms.ModelChoiceField(queryset=Asistente.objects.all(), label='Asistente', required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    activo = forms.ChoiceField(label='Estado', choices=[(True, 'En Proceso'), (False, 'Finalizada')], widget=forms.RadioSelect(attrs={'class': 'form-check'}))

    titulo = forms.CharField(label='Título', max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    diagnostico = forms.CharField(label='Diagnóstico', max_length=250, widget=forms.Textarea(attrs={'class': 'form-control'}))
    tratamiento = forms.CharField(label='Tratamiento', max_length=250, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    fecha_propuesta = forms.DateField(
        label='Fecha Propuesta',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Check if instance exists and has a primary key
            if self.instance.activo:
                self.initial['activo'] = True  # Set initial value based on stored value
            else:
                self.initial['activo'] = False

    class Meta:
        model = Cita
        fields = ('paciente', 
                  'doctor', 
                  'asistente',
                  'activo', 
                  'titulo', 
                  'diagnostico', 
                  'tratamiento', 
                  'fecha_propuesta',)
        use_crispy_forms = True

class RecipeForm(forms.ModelForm):
    #cita = forms.ModelChoiceField(queryset=Cita.objects.all(), label='Cita asignada')
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.all(), label='Medicamento prescrito')
    cantidad_deseada = forms.IntegerField(label='Cantidad requerida', min_value=0, error_messages={'min_value': 'La cantidad debe ser mayor o igual a 0.'})

    def clean_cantidad_deseada(self):
        cantidad = self.cleaned_data['cantidad_deseada']
        if cantidad <= 0:
            raise ValidationError('La cantidad debe ser un número positivo mayor que cero.')
        return cantidad

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super(RecipeForm, self).__init__(*args, **kwargs)
        if pk:
            self.fields['cita'].initial = pk

        # Establecer el campo 'id_orden' como no editable
        self.fields['cita'].disabled = True

    class Meta:
        model = Recipe
        fields = ['cita', 'medicamento', 'cantidad_deseada', 'nota']

    

class PacienteForm(forms.ModelForm):
    

    nombre = forms.CharField(label='Nombre', max_length=200,widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(label='Apellido', max_length=200,widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexo = forms.ChoiceField(label="Género", choices=Paciente.SEXO)
    direccion = forms.CharField(label="Dirección", max_length=255, required=False)
    telefono = forms.CharField(label="Número de teléfono", max_length=12, required=False)
    cid = forms.CharField(label="Cédula de identidad", max_length=15, required=False)
    class Meta:
        model = Paciente
        fields = '__all__'
        use_crispy_forms = True
