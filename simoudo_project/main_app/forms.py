from django import forms

from django.core.exceptions import ValidationError
from .models import Cita, Medicamento, Doctor, Asistente, Recipe, Paciente, User


from django.core.validators import RegexValidator, EmailValidator 

from django.forms.widgets import MultiWidget, TextInput, Select


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

# Phone number validation using a regular expression for Venezuelan numbers
    telefono = forms.CharField(label="Número de teléfono", max_length=12, required=False,
                                validators=[
                                    # Updated regex for phone number validation
                                    RegexValidator(regex=r'^(0414|0424|0412|0416|0426|0291)[-][0-9]{7}$', message='Ingrese un número de teléfono venezolano Valido. Ejemplo: 0412-5921110'),
                                    RegexValidator(regex=r'^[0-9-]+$', message='No se permiten letras en el número de teléfono')
                                ])

    # CID validation using separate fields for type and numeric part
    cid_tipo = forms.ChoiceField(label="Tipo de cédula", choices=[('V', 'V'), ('E', 'E')], widget=Select(attrs={'class': 'form-control cid-tipo'}), required=True)
    cid_numero = forms.CharField(label="Número de cédula", max_length=10,widget=TextInput(attrs={'class': 'form-control cid-numero'}) ,required=True,
                            validators=[RegexValidator(regex=r'^\d{7,9}$', message='Ingrese un número de cédula válido (solo números)')])

    email = forms.CharField(label="Correo electrónico", max_length=255, required=False, validators=[EmailValidator()], widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if instance exists (for editing)
        if self.instance:
            # Split the stored 'cid' value into 'cid_tipo' and 'cid_numero'
            if self.instance.cid:
                cid_tipo, cid_numero = self.instance.cid.split('-')
                self.initial['cid_tipo'] = cid_tipo
                self.initial['cid_numero'] = cid_numero

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.cid = f"{self.cleaned_data['cid_tipo']}-{self.cleaned_data['cid_numero']}"

        if commit:
            instance.save()
            return instance

    class Meta:
        model = Paciente
        fields = [
            'nombre',
            'apellido',
            'cid_tipo',  # Move cid_tipo below apellido
            'cid_numero',
            'sexo',
            'telefono',
            'email',
            'direccion',
            
        ]
        exclude = ['cid']
        use_crispy_forms = True
     
        
class DoctorForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(label='Apellido', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexo = forms.CharField(label='Género', max_length=10, widget=forms.Select(choices=Doctor.SEXO))

    
    # CID validation using separate fields for type and numeric part
    cid_tipo = forms.ChoiceField(label="Tipo de cédula", choices=[('V', 'V'), ('E', 'E')], widget=Select(attrs={'class': 'form-control cid-tipo'}), required=True)
    cid_numero = forms.CharField(label="Número de cédula", max_length=10,widget=TextInput(attrs={'class': 'form-control cid-numero'}) ,required=True,
                            validators=[RegexValidator(regex=r'^\d{7,9}$', message='Ingrese un número de cédula válido (solo números)')])
    
    
    forms.CharField(label="Número de teléfono", max_length=12, required=False,
                                validators=[
                                    # Updated regex for phone number validation
                                    RegexValidator(regex=r'^(0414|0424|0412|0416|0426|0291)[-][0-9]{7}$', message='Ingrese un número de teléfono venezolano Valido. Ejemplo: 0412-5921110'),
                                    RegexValidator(regex=r'^[0-9-]+$', message='No se permiten letras en el número de teléfono')
                                ])


    especialidad = forms.CharField(label='Especialidad', max_length=15, widget=forms.Select(choices=Doctor.ESPECIALIDAD))
    user_ref = forms.ModelChoiceField(label='Usuario Referenciado', queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label='Dirección (opcional)', max_length=250, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    notas = forms.CharField(label='Notas (opcional)', max_length=250, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Correo Electrónico (opcional)', max_length=255, validators=[EmailValidator()], required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if instance exists (for editing)
        if self.instance:
            # Split the stored 'cid' value into 'cid_tipo' and 'cid_numero'
            if self.instance.cid:
                cid_tipo, cid_numero = self.instance.cid.split('-')
                self.initial['cid_tipo'] = cid_tipo
                self.initial['cid_numero'] = cid_numero

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.cid = f"{self.cleaned_data['cid_tipo']}-{self.cleaned_data['cid_numero']}"

        if commit:
            instance.save()
            return instance

    class Meta:
        model = Doctor
        fields = ['nombre','apellido','sexo','cid_tipo','cid_numero','especialidad','telefono','email','direccion','user_ref', 'notas']  # You can still use this if you want to include all fields
        exclude = ['cid']
        use_crispy_forms = True
    # ... (Custom validation methods can go here as before)