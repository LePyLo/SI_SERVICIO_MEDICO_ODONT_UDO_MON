from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count

#Creo que dejare estas importanciones de esta forma de momento, pero bien pude importar todo
#pero para reducir la posibilidad de errores se importó asi.
from .models import Doctor, Paciente, Medicamento, Asistente, Cita, User, Recipe
from .forms import CitaForm, RecipeForm, PacienteForm

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
    return render(request, 'cita_insert_mod.html', context)

@login_required
def cita_modificar(request,pk):
    cita = get_object_or_404(Cita, pk=pk)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('citas')
    else:
        form = CitaForm(instance=cita)

    context = {'form': form, 'cita': cita, 'titulomain':'Modificar Cita Medica.'}
    return render(request, 'cita_insert_mod.html', context)

@login_required
def cita_eliminar(request):
    pass

@login_required
def cita_detail(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    cita_recipe = Recipe.objects.filter(cita=cita)
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
            messages.success(request, "Se registró el producto a la cita exitosamente.")
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
            return redirect('recipes', str(recipe.cita.id_cita))
    else:
        form = RecipeForm(instance=recipe)

    context = {'form': form, 'recipe': recipe, 'titulomain':'Modificar Elemento Cita Medica.'}
    return render(request, 'recipe_modificar.html', context)
    

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
    pass

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
    return render(request, 'cita_insert_mod.html', context)


@login_required
def paciente_modificar(request,pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    else:
        form = PacienteForm(instance=paciente)

    context = {'form': form, 'paciente': paciente, 'titulomain':'Modificar Datos de Paciente.', 'add_btn':'NO'}
    return render(request, 'cita_insert_mod.html', context)

@login_required
def paciente_eliminar(request,pk):
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