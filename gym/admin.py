from django.contrib import admin
from.models import Ejercicio, Rutina, EjercicioRutina, Entrenamiento, SerieEjercicio

# Register your models here.
admin.site.register(Ejercicio)
admin.site.register(Rutina)
admin.site.register(EjercicioRutina)
admin.site.register(Entrenamiento)
admin.site.register(SerieEjercicio)
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'peso_corporal')
    search_fields = ('usuario__username',)
