from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from datetime import date
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.conf import settings
from io import BytesIO
from xhtml2pdf import pisa 

#Creo que dejare estas importanciones de esta forma de momento, pero bien pude importar todo
#pero para reducir la posibilidad de errores se importó asi.
from .models import Doctor, Paciente, Medicamento, Asistente, Cita, User, Recipe
from .forms import CitaForm, RecipeForm, PacienteForm, DoctorForm, AsistenteForm, MedicamentoForm

######################################################################################
######################################################################################
#CONTROLADORES RELACIONADOS CON CITAS
@login_required
def cita_obtener_todas(request):
    lista_citas = Cita.objects.all().annotate(recipe_count=Count('recipe'))
    return render(request, 'citas.html',{'citas':lista_citas, 'titulo_web':'Citas - SIMOUDO'})

@login_required
def cita_insertar(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            cita = form.save(commit=False)
            cita.creado_por = request.user
            cita.save()
            messages.success(request, "La cita se creó exitosamente.")
            return redirect('citas')

        if request.POST.get('guardar_e_insertar_medicamento' ) and form.is_valid() :
            cita = form.save(commit=False)
            cita.creado_por = request.user
            cita.save()
            pk_cita = cita.pk
            url = reverse('recipe_insertar', kwargs={'pk': pk_cita})
            messages.success(request, "La cita se creó exitosamente.")
            return redirect(url)
    else:
        form = CitaForm()
    context = {'form': form, 'titulomain':'Crear nueva cita Medica.', 'add_btn':'YES'}
    return render(request, 'insert_mod_temp.html', context)

@login_required
def cita_modificar(request,pk):
    cita = get_object_or_404(Cita, pk=pk)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.info(request, "Información de la Cita actualizada con éxito.")
            return redirect('citas')
    else:
        form = CitaForm(instance=cita)

    context = {'form': form, 'cita': cita, 'titulomain':'Modificar Cita Medica.'}
    return render(request, 'insert_mod_temp.html', context)

@login_required
def cita_eliminar(request):
    pass

@login_required
def cita_detail(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    cita_recipe = Recipe.objects.filter(cita=cita)
    if request.method == 'POST':
        
        
        context = {"titulo":cita.titulo, 
                   "paciente":cita.paciente.get_full_name(), 
                   "doctor":cita.doctor.get_full_name(),
                   "diagnostico":cita.diagnostico,
                   "tratamiento":cita.tratamiento,
                   "fecha_propuesta":cita.fecha_propuesta,
                   "recipe":cita_recipe,
                   "especialidad":cita.doctor.especialidad.capitalize(),
                   }
        return generar_pdf(request, context)

    context = {'cita':cita,'recipe_list':cita_recipe, 'titulo_web':'Cita en detalle'}
    return render(request, 'cita_detail.html',context)


@login_required
def recipe_insertar(request,pk):
    if request.method == 'POST':
        form = RecipeForm(request.POST, pk=pk)

        if request.POST.get("guardar_y_regresar") and form.is_valid():
            recipe = form.save(commit=False)
            recipe.cita = Cita.objects.get(pk=pk)
            recipe.save()
            messages.success(request, "Se registró el medicamento a la cita exitosamente.")
            return redirect('citas') 

        elif request.POST.get("guardar_y_crear_otro") and form.is_valid():
            recipe = form.save(commit=False)
            recipe.cita = Cita.objects.get(pk=pk)
            recipe.save()
            messages.success(request, "Se registró el medicamento a la cita exitosamente.")
            form = RecipeForm(pk=pk)

    else:
        form = RecipeForm(pk=pk)

    return render(request, 'recipe_insert.html', {'form': form, 'titulo_web': 'Añadir Medicamentos a Recipe de Cita Medica'})

@login_required
def recipe_listar(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    cita_recipe = Recipe.objects.filter(cita=cita)


    context={'cita':cita, 'recipe':cita_recipe,
             'titulo_web':'Recipe de Cita Medica ',}

    return render(request, 'recipes.html', context)


@login_required
def recipe_modificar(request,pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.info(request, "Elemento de recipe de cita actualizado con éxito.")
            return redirect('recipes', str(recipe.cita.id_cita))
    else:
        form = RecipeForm(instance=recipe)

    context = {'form': form, 'recipe': recipe, 'titulomain':'Modificar Elemento Cita Medica.'}
    return render(request, 'recipe_modificar.html', context)
    

@login_required
def cita_enviar_email(request, cita_pk):
    cita = get_object_or_404(Cita, pk=cita_pk)
    context = {
    "receiver_name": cita.paciente.get_full_name(),
    "cita_propuesta":cita.fecha_propuesta,
    "cita_doctor": cita.doctor.get_full_name(),
    "cita_area":cita.doctor.especialidad.capitalize(),
    "cita_doctor_tlf":cita.doctor.telefono,
    "cita_emision":cita.fecha_creacion,
    "fecha_email":date.today(),
    }
    receiver_mail = str(cita.paciente.email).strip()

    html_body =  render_to_string(
        "email_cita_info.html",
        context
    )

    sended_mail = send_mail(subject="Recordatorio para Cita Medica en el Centro Medico odontologico UDO Monagas.",
                            message=".", 
                            html_message=html_body,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[receiver_mail],
                            fail_silently=False,
                            )


    if (sended_mail):
        messages.success(request, "Correo enviado exitosamente al paciente.")
    else:
        messages.error(request, "Ocurrio un error inesperado al tratar de enviar un correo al paciente.")

    return HttpResponseRedirect(reverse('citas')) 




@login_required
def generar_pdf(request, context):

    # Renderizar la plantilla HTML con los datos
    template = get_template('cita_pdf_export.html')

    html = template.render(context)

    # Configuración de xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{context["titulo"]}_{context["paciente"]}_{date.today()}.pdf"'

    result = pisa.CreatePDF(html, dest=response)

    if result.err:
        return HttpResponse('Error: %s' % result.err)
    else:
        return response
    

######################################################################################
######################################################################################
#CONTROLADORES RELACIONADOS CON PACIENTES

@login_required
def paciente_obtener_todos(request):
    pacientes = Paciente.objects.all().annotate(cita_count=Count('cita'))
    context = {'pacientes':pacientes, 'titulo_web':'Listado de Pacientes Registrados.'}
    return render(request, 'pacientes.html', context)

@login_required
def paciente_detail(request,pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    historial = Cita.objects.filter(paciente=paciente)

    context = {'paciente':paciente,
               'historial':historial,
               'titulo_web':'Información del Paciente: '+str(paciente.get_full_name())}
    return render(request, 'paciente_detail.html', context)

@login_required
def paciente_insertar(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            form.save()
            messages.success(request, "Paciente registrado exitosamente.")
            return redirect('pacientes')

    else:
        form = PacienteForm()
    context = {'form': form, 'titulomain':'Registrar nuevo paciente.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)


@login_required
def paciente_modificar(request,pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.info(request, "Información de Paciente actualizada exitosamente.")
            return redirect('pacientes')
    else:
        form = PacienteForm(instance=paciente)

    context = {'form': form, 'paciente': paciente, 'titulomain':'Modificar Datos de Paciente.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)

@login_required
def paciente_eliminar(request,pk):
    pass

######################################################################################
######################################################################################
# CONTROLADORES RELACIONADOS CON DOCTORES.
@login_required
def doctor_obtener_todos(request):
    doctores = Doctor.objects.all().annotate(cita_count=Count('cita'))
    context = {'doctores':doctores, 'titulo_web':'Listado de Doctores Registrados.'}
    return render(request, 'doctores.html', context)


@login_required
def doctor_detail(request,pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    context = {'doctor':doctor,
               'titulo_web':'Información del Doctor: '+str(doctor.get_full_name())}
    return render(request, 'doctor_detail.html', context)

@login_required
def doctor_insertar(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            form.save()
            messages.success(request, "Doctor registrado exitosamente.")
            return redirect('doctores')

    else:
        form = DoctorForm()
    context = {'form': form, 'titulomain':'Registrar Nuevo Doctor.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)


@login_required
def doctor_modificar(request,pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.info(request, "Información de doctor actualizada exitosamente.")
            return redirect('doctores')
    else:
        form = DoctorForm(instance=doctor)

    context = {'form': form, 'doctor': doctor, 'titulomain':'Modificar Datos de Doctor.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)

@login_required
def doctor_eliminar(request,pk):
    pass


######################################################################################
######################################################################################
# CONTROLADORES RELACIONADOS CON ASISTENTES MEDICOS.
@login_required
def asistente_obtener_todos(request):
    asistentes = Asistente.objects.all()
    context = {'asistentes':asistentes, 'titulo_web':'Listado de Asistentes Medicos Registrados.'}
    return render(request, 'asistentes.html', context)


@login_required
def asistente_detail(request,pk):
    asistente_medico = get_object_or_404(Asistente, pk=pk)
    context = {'asistente':asistente_medico,
               'titulo_web':'Información del Asistente Medico: '+str(asistente_medico.get_full_name())}
    return render(request, 'asistente_detail.html', context)

@login_required
def asistente_insertar(request):
    if request.method == 'POST':
        form = AsistenteForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            form.save()
            messages.success(request, "Asistente Medico registrado exitosamente.")
            return redirect('asistentes')

    else:
        form =AsistenteForm()
    context = {'form': form, 'titulomain':'Registrar Nuevo Asistente medico.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)


@login_required
def asistente_modificar(request,pk):
    asistente = get_object_or_404(Asistente, pk=pk)

    if request.method == 'POST':
        form = AsistenteForm(request.POST, instance=asistente)
        if form.is_valid():
            form.save()
            messages.info(request, "Información de Asistente Medico actualizada exitosamente.")
            return redirect('asistentes')
    else:
        form = AsistenteForm(instance=asistente)

    context = {'form': form, 'asistente': asistente, 'titulomain':'Modificar Datos de Asistente Medico.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)

@login_required
def asistente_eliminar(request,pk):
    pass

######################################################################################
######################################################################################
# CONTROLADORES RELACIONADOS CON MEDICAMENTOS.
@login_required
def medicamento_obtener_todos(request):
    medicamentos = Medicamento.objects.all()
    context = {'medicamentos':medicamentos, 'titulo_web':'Listado de Medicamentos Registrados.'}
    return render(request, 'medicamentos.html', context)


@login_required
def medicamento_detail(request,pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    context = {'medicamento':medicamento,
               'titulo_web':'Información del Medicamento: '+str(medicamento.nombre)}
    return render(request, 'medicamento_detail.html', context)

@login_required
def medicamento_insertar(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if request.POST.get('guardar_y_regresar' )  and form.is_valid() :
            form.save()
            messages.success(request, "Medicamento añadido exitosamente.")
            return redirect('medicamentos')

    else:
        form =MedicamentoForm()
    context = {'form': form, 'titulomain':'Registrar Nuevo Medicamento.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)

@login_required
def medicamento_modificar(request,pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)

    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.info(request, "Datos de Medicamento actualizados con éxito.")
            return redirect('medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)

    context = {'form': form, 'medicamento': medicamento, 'titulomain':'Modificar Datos de Medicamento.', 'add_btn':'NO'}
    return render(request, 'insert_mod_temp.html', context)

@login_required
def medicamento_eliminar(request,pk):
    pass

######################################################################################
######################################################################################
@login_required
def x_obtener_todos(request):
    pass

@login_required
def x_detail(request,pk):
    pass

@login_required
def x_insertar(request):
    pass

@login_required
def x_modificar(request,pk):
    pass

@login_required
def x_eliminar(request,pk):
    pass



######################################################################################
######################################################################################
#CONTROLADORES RELACIONADOS CON SESIONES DE USUARIOS

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Has iniciado sesión correctamente.")
        else:
            messages.warning(request, "Usuario o contraseña incorrectos.")
    if request.user.is_authenticated:
        
        return redirect('citas')
    
    context = {'page_name':"INICIO DE SESIÓN SIMO"}
    return render(request, 'login.html', context)

#Terminar sesión
def logout_user(request):
    logout(request)
    messages.success(request, "Te has desconectado correctamente")
    return HttpResponseRedirect(reverse('login')) 


######################################################################################
######################################################################################

#manejo de errores 404 custom
def custom_404(request, exception):
    return render(request, 'base/error_404.html', status=404)