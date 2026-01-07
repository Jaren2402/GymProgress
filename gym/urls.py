from django.urls import path
from.views import home, registro, login_view, logout_view, dashboard, lista_rutinas, crear_rutina, editar_rutina, eliminar_rutina, detalle_rutina, agregar_ejercicio_rutina, iniciar_entrenamiento, registrar_serie, finalizar_entrenamiento, historial_entrenamientos, progreso_dashboard, progreso_ejercicio

urlpatterns = [
    path('', home, name='home'),
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('login/', logout_view, name='logout'),
    path('rutinas/', lista_rutinas, name='lista_rutinas'),
    path('rutinas/crear', crear_rutina, name='crear_rutina'),
    path('rutinas/editar/<int:rutina_id>/', editar_rutina, name='editar_rutina'),
    path('rutinas/eliminar/<int:rutina_id>/', eliminar_rutina, name='eliminar_rutina'),
    path('rutinas/<int:rutina_id>/', detalle_rutina, name='detalle_rutina'),
    path('rutinas/<int:rutina_id>/agregar-ejercicio/', agregar_ejercicio_rutina, name='agregar_ejercicio_rutina'),
    path('entrenamientos/iniciar/<int:rutina_id>/', iniciar_entrenamiento, name='iniciar_entrenamiento'),
    path('entrenamientos/registrar/<int:entrenamiento_id>/', registrar_serie, name='registrar_serie'),
    path('entrenamientos/finalizar/<int:entrenamiento_id>/', finalizar_entrenamiento, name='finalizar_entrenamiento'),
    path('entrenamientos/historial/', historial_entrenamientos, name='historial_entrenamientos'),
    path('progreso/', progreso_dashboard, name='progreso_dashboard'),
    path('progreso/ejercicio/<int:ejercicio_id>/', progreso_ejercicio, name='progreso_ejercicio'),
]




