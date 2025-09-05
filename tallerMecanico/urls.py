"""
URL configuration for tallerMecanico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vehiculos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('buscar/', views.buscar_vehiculo, name='buscar_vehiculo'),
    path('vehiculo/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('vehiculo/<int:vehiculo_id>/editar/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculo/<int:vehiculo_id>/agregar/', views.agregar_reparacion, name='agregar_reparacion'),
    path('reparacion/<int:reparacion_id>/editar/', views.editar_reparacion, name='editar_reparacion'),
    path('presupuestos/', views.generar_presupuestos, name='generar_presupuestos'),
    path('presupuesto/<int:vehiculo_id>/<str:tipo>/', views.generar_pdf_presupuesto, name='generar_pdf_presupuesto'),
]

