from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# MODELO 1: Ejercicio - Catálogo de ejercicios disponibles
class Ejercicio(models.Model):
    # Opciones para choices (dropdowns)
    GRUPO_MUSCULAR_CHOICES = [
        ('pecho', 'Pecho'),
        ('espalda', 'Espalda'),
        ('piernas', 'Piernas'),
        ('hombros', 'Hombros'),
        ('brazos', 'Brazos'),
        ('core', 'Core'),
        ('cardio', 'Cardio'),
    ]
    
    # Campos de la tabla
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    grupo_muscular = models.CharField(max_length=20, choices=GRUPO_MUSCULAR_CHOICES)
    imagen = models.CharField(max_length=200, blank=True)  # Para emoji o URL
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

# MODELO 2: Rutina - Conjunto de ejercicios
class Rutina(models.Model):
    # Relación: Una rutina pertenece a un usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Campos
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    # Estado
    activa = models.BooleanField(default=True)
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"

# MODELO 3: EjercicioRutina - Ejercicios dentro de una rutina
class EjercicioRutina(models.Model):
    # Relaciones
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    
    # Configuración del ejercicio en esta rutina
    series = models.IntegerField(default=3)
    repeticiones = models.CharField(max_length=50, default="8-12")  # Ej: "8-12", "15-20"
    descanso = models.FloatField(default=1.5)  # Segundos entre series
    
    # Orden en la rutina
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']

# MODELO 4: Entrenamiento - Sesión de gym realizada
class Entrenamiento(models.Model):
    # Relaciones
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    
    # Fecha y duración
    fecha = models.DateTimeField(auto_now_add=True)
    duracion_minutos = models.IntegerField(default=0)
    
    # Notas del usuario
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rutina.nombre} - {self.fecha.date()}"

# MODELO 5: SerieEjercicio - Series realizadas en un entrenamiento
class SerieEjercicio(models.Model):
    # Relaciones
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE, related_name='series')
    ejercicio_rutina = models.ForeignKey(EjercicioRutina, on_delete=models.CASCADE)
    
    # Datos de la serie realizada
    numero_serie = models.IntegerField()  # Serie 1, 2, 3...
    peso_kg = models.FloatField()         # Peso utilizado
    repeticiones = models.IntegerField()  # Reps realizadas
    
    class Meta:
        ordering = ['ejercicio_rutina__orden', 'numero_serie']