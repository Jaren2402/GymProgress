from django import forms
from .models import Rutina, Ejercicio, EjercicioRutina

# 📝 EXPLICACIÓN: ¿Por qué crear un Form?
# Django forms nos ayudan con:
# - Validación automática
# - Renderizado HTML
# - Protección contra ataques

class RutinaForm(forms.ModelForm):
    # ¿POR QUÉ ModelForm? Porque se basa en un modelo existente
    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion']
        # ↑ ¿Qué campos del modelo vamos a usar?
        
        # Personalizar los labels
        labels = {
            'nombre': 'Nombre de la Rutina',
            'descripcion': 'Descripción (opcional)',
        }
        
        # Personalizar los widgets (cómo se ven los inputs)
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control dark-input',
                'placeholder': 'Ej: Rutina Pierna, Full Body...'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control dark-input',
                'rows': 3,
                'placeholder': 'Describe tu rutina...'
            }),
        }
        
class EjercicioRutinaForm(forms.ModelForm):
    # 📝 EXPLICACIÓN: Este form es para agregar ejercicios a una rutina específica
    
    class Meta:
        model = EjercicioRutina
        fields = ['ejercicio', 'series', 'repeticiones', 'descanso', 'orden']
        
        # Personalizar labels
        labels = {
            'ejercicio': 'Ejercicio',
            'series': 'Número de Series',
            'repeticiones': 'Repeticiones (ej: 8-12)',
            'descanso': 'Descanso entre series (minutos)',
            'orden': 'Orden en la rutina'
        }
        
        # Personalizar widgets
        widgets = {
            'ejercicio': forms.Select(attrs={
                'class': 'form-control dark-input'
            }),
            'series': forms.NumberInput(attrs={
                'class': 'form-control dark-input',
                'min': 1,
                'max': 10
            }),
            'repeticiones': forms.TextInput(attrs={
                'class': 'form-control dark-input',
                'placeholder': '8-12, 15-20, 5-8...'
            }),
            'descanso': forms.NumberInput(attrs={
                'class': 'form-control dark-input',
                'min': 0.5,
                'max': 5,
                'step': 0.5,
                'placeholder': '1.5 (1 minuto 30 segundos)'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control dark-input',
                'min': 0
            }),
        }