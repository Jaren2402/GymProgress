from django.shortcuts import render, redirect, get_object_or_404
from.models import Rutina, Ejercicio, EjercicioRutina, Entrenamiento, SerieEjercicio
from.forms import RutinaForm, EjercicioRutinaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Página principal
def home(request):
    return render(request, 'home.html')

# REGISTRO - con lógica real
def registro(request):
    # Si el usuario envió el formulario (POST)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Guardar usuario en la base de datos
            user = form.save()
            
            # Mensaje de éxito
            messages.success(request, f'¡Cuenta creada para {user.username}! Ahora puedes iniciar sesión.')
            
            # Redirigir al login
            return redirect('login')
    else:
        # Si el usuario solo está viendo la página (GET)
        form = UserCreationForm()
    
    return render(request, 'registro.html', {'form': form})

# LOGIN - con lógica real  
def login_view(request):
    # Si el usuario envió el formulario (POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Verificar si el usuario existe y la contraseña es correcta
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si las credenciales son correctas, iniciar sesión
            login(request, user)
            return redirect('dashboard')
        else:
            # Si las credenciales son incorrectas
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

# LOGOUT
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('home')

# DASHBOARD - Solo para usuarios logueados
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# 📊 VIEW: Lista de rutinas del usuario
@login_required
def lista_rutinas(request):
    # 📝 EXPLICACIÓN: ¿Qué hace esta view?
    # 1. Obtener TODAS las rutinas del usuario actual
    # 2. Filtrar solo las activas
    # 3. Pasarlas al template para mostrar
    
    rutinas = Rutina.objects.filter(
        usuario=request.user, 
        activa=True
    ).order_by('-fecha_creacion')
    # ↑ ¿POR QUÉ este query?
    # - usuario=request.user → Solo rutinas del usuario logueado
    # - activa=True → Solo rutinas no "eliminadas"  
    # - order_by('-fecha_creacion') → Más recientes primero
    
    return render(request, 'rutinas/lista.html', {
        'rutinas': rutinas
    })

# ➕ VIEW: Crear nueva rutina
@login_required
def crear_rutina(request):
    # 📝 EXPLICACIÓN: Patrón clásico de formularios Django
    # GET → Mostrar formulario vacío
    # POST → Procesar datos del formulario
    
    if request.method == 'POST':
        # ¿POR QUÉ request.POST? Porque el usuario envió datos
        form = RutinaForm(request.POST)
        
        if form.is_valid():
            # 📝 EXPLICACIÓN: ¿Por qué commit=False?
            # form.save() guardaría PERO sin el usuario
            # commit=False → Crea el objeto pero no guarda en BD todavía
            rutina = form.save(commit=False)
            
            # Asignar el usuario actual (importante para la relación)
            rutina.usuario = request.user
            
            # Ahora sí guardar en la base de datos
            rutina.save()
            
            # Mensaje de éxito y redirigir
            messages.success(request, '¡Rutina creada exitosamente!')
            return redirect('lista_rutinas')
    else:
        # GET request → Mostrar formulario vacío
        form = RutinaForm()
    
    return render(request, 'rutinas/crear.html', {
        'form': form,
        'titulo': 'Crear Nueva Rutina'
    })

# ✏️ VIEW: Editar rutina existente
@login_required
def editar_rutina(request, rutina_id):
    # 📝 EXPLICACIÓN: get_object_or_404 vs Rutina.objects.get()
    # get_object_or_404 es MÁS SEGURO → Si no existe, muestra 404
    # Además filtramos por usuario para seguridad
    
    rutina = get_object_or_404(
        Rutina, 
        id=rutina_id, 
        usuario=request.user,  # ¡IMPORTANTE! Seguridad
        activa=True            # Solo editar rutinas activas
    )
    
    if request.method == 'POST':
        # instance=rutina → Rellena el form con datos existentes
        form = RutinaForm(request.POST, instance=rutina)
        
        if form.is_valid():
            form.save()
            messages.success(request, '¡Rutina actualizada!')
            return redirect('lista_rutinas')
    else:
        # GET → Mostrar form con datos actuales
        form = RutinaForm(instance=rutina)
    
    return render(request, 'rutinas/crear.html', {
        'form': form,
        'titulo': 'Editar Rutina',
        'rutina': rutina
    })

# 🗑️ VIEW: "Eliminar" rutina (soft delete)
@login_required  
def eliminar_rutina(request, rutina_id):
    rutina = get_object_or_404(
        Rutina, 
        id=rutina_id, 
        usuario=request.user,
        activa=True
    )
    
    # 📝 EXPLICACIÓN: ¿Por qué no usamos rutina.delete()?
    # Porque queremos SOFT DELETE → mantener el historial
    # Simplemente cambiamos activa=False
    
    rutina.activa = False
    rutina.save()
    
    messages.success(request, 'Rutina eliminada')
    return redirect('lista_rutinas')

# 📝 EXPLICACIÓN: Esta view muestra una rutina específica con TODOS sus ejercicios
@login_required
def detalle_rutina(request, rutina_id):
    # Obtener la rutina (con seguridad - solo del usuario actual)
    rutina = get_object_or_404(
        Rutina, 
        id=rutina_id, 
        usuario=request.user,
        activa=True
    )
    
    # Obtener todos los ejercicios de esta rutina, ordenados
    ejercicios = rutina.ejercicios.all().order_by('orden')
    
    return render(request, 'rutinas/detalle.html', {
        'rutina': rutina,
        'ejercicios': ejercicios
    })
    
# 📝 EXPLICACIÓN: Esta view permite agregar ejercicios a una rutina existente
@login_required
def agregar_ejercicio_rutina(request, rutina_id):
    # Verificar que la rutina existe y pertenece al usuario
    rutina = get_object_or_404(
        Rutina, 
        id=rutina_id, 
        usuario=request.user,
        activa=True
    )
    
    if request.method == 'POST':
        # Crear form con los datos enviados
        form = EjercicioRutinaForm(request.POST)
        
        if form.is_valid():
            # Guardar pero no commit (para asignar la rutina)
            ejercicio_rutina = form.save(commit=False)
            ejercicio_rutina.rutina = rutina  # Asignar a la rutina actual
            ejercicio_rutina.save()
            
            messages.success(request, f'Ejercicio agregado a {rutina.nombre}')
            return redirect('detalle_rutina', rutina_id=rutina.id)
    else:
        # Mostrar form vacío
        form = EjercicioRutinaForm()
    
    return render(request, 'rutinas/agregar_ejercicio.html', {
        'form': form,
        'rutina': rutina
    })
    
# 📝 EXPLICACIÓN: Inicia un nuevo entrenamiento basado en una rutina
@login_required
def iniciar_entrenamiento(request, rutina_id):
    # Obtener la rutina (solo del usuario actual)
    rutina = get_object_or_404(
        Rutina, 
        id=rutina_id, 
        usuario=request.user,
        activa=True
    )
    
    # Crear un nuevo entrenamiento
    entrenamiento = Entrenamiento.objects.create(
        usuario=request.user,
        rutina=rutina
    )
    
    # Redirigir a la página para registrar series
    return redirect('registrar_serie', entrenamiento_id=entrenamiento.id)

# 📝 EXPLICACIÓN: Registra serie por serie durante el entrenamiento
@login_required
def registrar_serie(request, entrenamiento_id):
    # Obtener el entrenamiento actual
    entrenamiento = get_object_or_404(
        Entrenamiento,
        id=entrenamiento_id,
        usuario=request.user
    )
    
    # Obtener todos los ejercicios de la rutina
    ejercicios_rutina = entrenamiento.rutina.ejercicios.all().order_by('orden')
    
    # Determinar qué ejercicio toca ahora
    # Lógica: buscar el primer ejercicio sin series registradas hoy
    ejercicio_actual = None
    for ejercicio_rutina in ejercicios_rutina:
        series_registradas = SerieEjercicio.objects.filter(
            entrenamiento=entrenamiento,
            ejercicio_rutina=ejercicio_rutina
        ).count()
        
        if series_registradas < ejercicio_rutina.series:
            ejercicio_actual = ejercicio_rutina
            numero_serie = series_registradas + 1
            break
    
    # Si no hay más ejercicios, terminar entrenamiento
    if not ejercicio_actual:
        return redirect('finalizar_entrenamiento', entrenamiento_id=entrenamiento.id)
    
    # Procesar el formulario si se envió
    if request.method == 'POST':
        peso = float(request.POST.get('peso', 0))
        repeticiones = int(request.POST.get('repeticiones', 0))
        
        # Crear registro de la serie
        SerieEjercicio.objects.create(
            entrenamiento=entrenamiento,
            ejercicio_rutina=ejercicio_actual,
            numero_serie=numero_serie,
            peso_kg=peso,
            repeticiones=repeticiones
        )
        
        # Redirigir a la misma página para la siguiente serie
        return redirect('registrar_serie', entrenamiento_id=entrenamiento.id)
    
    # Contexto para el template
    return render(request, 'entrenamientos/registrar_serie.html', {
        'entrenamiento': entrenamiento,
        'ejercicio_actual': ejercicio_actual,
        'numero_serie': numero_serie,
        'series_completadas': numero_serie - 1,
        'total_series': ejercicio_actual.series
    })
    
# 📝 EXPLICACIÓN: Muestra resumen del entrenamiento completado
@login_required
def finalizar_entrenamiento(request, entrenamiento_id):
    entrenamiento = get_object_or_404(
        Entrenamiento,
        id=entrenamiento_id,
        usuario=request.user
    )
    
    # Calcular duración aproximada (podríamos mejorarlo con timestamps)
    # Por ahora, un cálculo simple
    entrenamiento.duracion_minutos = 60  # Valor de ejemplo
    entrenamiento.save()
    
    # Obtener todas las series de este entrenamiento
    series = SerieEjercicio.objects.filter(
        entrenamiento=entrenamiento
    ).order_by('ejercicio_rutina__orden', 'numero_serie')
    
    return render(request, 'entrenamientos/finalizar.html', {
        'entrenamiento': entrenamiento,
        'series': series
    })
    
# 📝 EXPLICACIÓN: Muestra todos los entrenamientos del usuario
@login_required
def historial_entrenamientos(request):
    entrenamientos = Entrenamiento.objects.filter(
        usuario=request.user
    ).order_by('-fecha')
    
    return render(request, 'entrenamientos/historial.html', {
        'entrenamientos': entrenamientos
    })
    
# 📝 EXPLICACIÓN: Calcula el progreso de un ejercicio específico
def calcular_progreso_ejercicio(usuario, ejercicio_id):
    """
    Compara el rendimiento actual vs anterior en un ejercicio específico
    """
    # Obtener todas las series de este ejercicio para el usuario
    series = SerieEjercicio.objects.filter(
        ejercicio_rutina__ejercicio_id=ejercicio_id,
        entrenamiento__usuario=usuario
    ).order_by('entrenamiento__fecha')
    
    if not series:
        return None  # No hay datos para este ejercicio
    
    # Agrupar por entrenamiento
    progreso_por_entrenamiento = []
    entrenamiento_actual = None
    datos_entrenamiento = {}
    
    for serie in series:
        if serie.entrenamiento != entrenamiento_actual:
            if datos_entrenamiento:
                progreso_por_entrenamiento.append(datos_entrenamiento)
            
            entrenamiento_actual = serie.entrenamiento
            datos_entrenamiento = {
                'fecha': serie.entrenamiento.fecha,
                'rutina': serie.entrenamiento.rutina.nombre,
                'peso_maximo': 0,
                'reps_totales': 0,
                'series_completadas': 0,
                'volumen_total': 0  # peso x reps
            }
        
        # Actualizar estadísticas
        datos_entrenamiento['peso_maximo'] = max(
            datos_entrenamiento['peso_maximo'], 
            serie.peso_kg
        )
        datos_entrenamiento['reps_totales'] += serie.repeticiones
        datos_entrenamiento['series_completadas'] += 1
        datos_entrenamiento['volumen_total'] += serie.peso_kg * serie.repeticiones
    
    if datos_entrenamiento:
        progreso_por_entrenamiento.append(datos_entrenamiento)
    
    return progreso_por_entrenamiento

# 📝 EXPLICACIÓN: Encuentra PRs (Personal Records) del usuario
def encontrar_prs(usuario):
    """
    Encuentra los récords personales del usuario en cada ejercicio
    """
    prs = []
    
    # Obtener todos los ejercicios que el usuario ha hecho
    ejercicios_hechos = Ejercicio.objects.filter(
        ejerciciorutina__rutina__entrenamiento__usuario=usuario
    ).distinct()
    
    for ejercicio in ejercicios_hechos:
        # Encontrar la serie con máximo peso para este ejercicio
        max_serie = SerieEjercicio.objects.filter(
            ejercicio_rutina__ejercicio=ejercicio,
            entrenamiento__usuario=usuario
        ).order_by('-peso_kg').first()
        
        if max_serie:
            prs.append({
                'ejercicio': ejercicio.nombre,
                'peso': max_serie.peso_kg,
                'reps': max_serie.repeticiones,
                'fecha': max_serie.entrenamiento.fecha,
                'ejercicio_id': ejercicio.id
            })
    
    return prs

# 📝 EXPLICACIÓN: Calcula estadísticas generales del usuario
def calcular_estadisticas_generales(usuario):
    """
    Calcula estadísticas generales de todos los entrenamientos
    """
    entrenamientos = Entrenamiento.objects.filter(usuario=usuario)
    
    if not entrenamientos:
        return None
    
    total_entrenamientos = entrenamientos.count()
    total_series = SerieEjercicio.objects.filter(
        entrenamiento__usuario=usuario
    ).count()
    
    # Encontrar el ejercicio más frecuente
    from django.db.models import Count
    ejercicio_frecuente = Ejercicio.objects.filter(
        ejerciciorutina__rutina__entrenamiento__usuario=usuario
    ).annotate(
        veces_realizado=Count('ejerciciorutina__rutina__entrenamiento')
    ).order_by('-veces_realizado').first()
    
    return {
        'total_entrenamientos': total_entrenamientos,
        'total_series': total_series,
        'ejercicio_frecuente': ejercicio_frecuente.nombre if ejercicio_frecuente else 'Ninguno',
        'primera_fecha': entrenamientos.order_by('fecha').first().fecha,
        'ultima_fecha': entrenamientos.order_by('-fecha').first().fecha,
    }
    
# 📝 EXPLICACIÓN: Vista principal de progreso
@login_required
def progreso_dashboard(request):
    """
    Dashboard principal con gráficos y estadísticas
    """
    # Obtener estadísticas generales
    estadisticas = calcular_estadisticas_generales(request.user)
    
    # Obtener PRs del usuario
    prs = encontrar_prs(request.user)
    
    # Obtener últimos 5 entrenamientos para gráfico reciente
    ultimos_entrenamientos = Entrenamiento.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:5]
    
    # Preparar datos para gráficos
    datos_grafico = []
    for entrenamiento in ultimos_entrenamientos:
        series_entrenamiento = SerieEjercicio.objects.filter(
            entrenamiento=entrenamiento
        )
        if series_entrenamiento:
            volumen_total = sum(s.peso_kg * s.repeticiones for s in series_entrenamiento)
            datos_grafico.append({
                'fecha': entrenamiento.fecha.strftime('%d/%m'),
                'volumen': volumen_total,
                'nombre': entrenamiento.rutina.nombre
            })
    
    return render(request, 'progreso/dashboard.html', {
        'estadisticas': estadisticas,
        'prs': prs,
        'datos_grafico': datos_grafico,
        'ultimos_entrenamientos': ultimos_entrenamientos
    })

# 📝 EXPLICACIÓN: Vista detallada de progreso por ejercicio
@login_required
def progreso_ejercicio(request, ejercicio_id):
    """
    Muestra el progreso detallado de un ejercicio específico
    """
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    
    # Calcular progreso histórico
    historial = calcular_progreso_ejercicio(request.user, ejercicio_id)
    
    # Preparar datos para gráfico
    datos_grafico = []
    if historial:
        for punto in historial[-10:]:  # Últimos 10 puntos
            datos_grafico.append({
                'fecha': punto['fecha'].strftime('%d/%m'),
                'peso_maximo': punto['peso_maximo'],
                'volumen': punto['volumen_total']
            })
    
    return render(request, 'progreso/ejercicio.html', {
        'ejercicio': ejercicio,
        'historial': historial,
        'datos_grafico': datos_grafico
    })