# 🏋️‍♂️ GymProgress

Aplicación web para seguimiento de progreso en entrenamientos de fuerza.


## 🚀 Características Principales

- **Registro de usuarios** con autenticación segura
- **Gestión de rutinas** personalizadas
- **Registro de entrenamientos** en tiempo real
- **Análisis automático** de progreso
- **Dashboard** con estadísticas y gráficos
- **Interfaz responsive** (funciona en móviles)


## 🛠️ Tecnologías Utilizadas

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Base de datos:** SQLite
- **Autenticación:** Sistema nativo de Django

## 📁 Estructura del Proyecto

gymprogress/
├──gym/                    # Aplicación principal
│├── models.py             # Modelos de base de datos
│├── views.py              # Lógica de negocio
│├── templates/            # Plantillas HTML
│└── urls.py               # Rutas de la app
├──gymprogress_project/    # Configuración del proyecto
└──manage.py               # Script de administración


## ⚡ Cómo Ejecutar Localmente

1. Clonar repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Mac/Linux)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Ejecutar migraciones: `python manage.py migrate`
6. Crear superusuario: `python manage.py createsuperuser`
7. Ejecutar servidor: `python manage.py runserver`

Visitar: http://127.0.0.1:8000/


## 👤 Flujo de Usuario

1. **Registro/Login** → Crear cuenta o iniciar sesión
2. **Crear rutinas** → Diseñar planes de entrenamiento
3. **Registrar entrenamientos** → Trackear lo realizado
4. **Ver progreso** → Analizar estadísticas y gráficos


## 🎯 Objetivo del Proyecto

Solución tecnológica para el problema de **pérdida de seguimiento de progreso** en entrenamientos de fuerza, proporcionando **datos objetivos** de evolución.


## 📄 Licencia

Proyecto académico - UNEFA