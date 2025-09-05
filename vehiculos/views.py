from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Max
from .models import Vehiculo
from .models import HistorialReparacion
from .forms import HistorialReparacionForm, VehiculoForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from decimal import Decimal

def index(request):
    return render(request, 'index.html')

def buscar_vehiculo(request):
    query = request.GET.get("q", "")
    vehiculos = Vehiculo.objects.filter(placa__icontains=query) if query else []

    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            nuevo = form.save()
            return redirect("detalle_vehiculo", vehiculo_id=nuevo.id)
    else:
        # si hay query, la ponemos como valor inicial en el campo placa
        initial_data = {"placa": query} if query else {}
        form = VehiculoForm(initial=initial_data)

    return render(request, "buscar_vehiculo.html", {
        "query": query,
        "vehiculos": vehiculos,
        "form": form,
    })

def detalle_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    historiales = vehiculo.historiales.all().order_by('-fecha')
    return render(request, 'detalle_vehiculo.html', {
        'vehiculo': vehiculo,
        'historiales': historiales
    })

def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('detalle_vehiculo', vehiculo_id=vehiculo.id)
    else:
        form = VehiculoForm(instance=vehiculo)
    
    return render(request, 'form_vehiculo.html', {'form': form, 'vehiculo': vehiculo, 'accion': 'Editar'})


def agregar_reparacion(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    
    # Obtener todos los tipos de reparación únicos de este vehículo
    tipos_existentes = vehiculo.historiales.values_list('tipo_reparacion', flat=True).distinct()
    
    if request.method == 'POST':
        form = HistorialReparacionForm(request.POST)
        if form.is_valid():
            reparacion = form.save(commit=False)
            reparacion.vehiculo = vehiculo
            reparacion.save()
            return redirect('detalle_vehiculo', vehiculo_id=vehiculo.id)
    else:
        form = HistorialReparacionForm()
    
    return render(request, 'form_reparacion.html', {
        'form': form,
        'vehiculo': vehiculo,
        'accion': 'Agregar',
        'tipos_existentes': tipos_existentes
    })


def editar_reparacion(request, reparacion_id):
    reparacion = get_object_or_404(HistorialReparacion, id=reparacion_id)
    vehiculo = reparacion.vehiculo
    tipos_existentes = vehiculo.historiales.values_list('tipo_reparacion', flat=True).distinct()

    if request.method == 'POST':
        form = HistorialReparacionForm(request.POST, instance=reparacion)
        if form.is_valid():
            form.save()
            return redirect('detalle_vehiculo', vehiculo_id=vehiculo.id)
    else:
        form = HistorialReparacionForm(instance=reparacion)

    return render(request, 'form_reparacion.html', {
        'form': form,
        'vehiculo': vehiculo,
        'accion': 'Editar',
        'tipos_existentes': tipos_existentes
    })


def generar_presupuestos(request):
    query = request.GET.get("q", "")
    vehiculos = Vehiculo.objects.filter(placa__icontains=query) if query else []

    # Si se selecciona un vehículo, mostramos los tipos de reparación
    vehiculo_seleccionado = None
    tipos_reparacion = []
    if 'vehiculo_id' in request.GET:
        vehiculo_seleccionado = get_object_or_404(Vehiculo, id=request.GET['vehiculo_id'])
        # Tomamos los tipos únicos de reparación, mostrando el más reciente primero
        tipos_reparacion = (vehiculo_seleccionado.historiales
                            .values('tipo_reparacion')
                            .annotate(ultima_fecha=Max('fecha'))
                            .order_by('-ultima_fecha'))

    return render(request, 'generar_presupuestos.html', {
        'query': query,
        'vehiculos': vehiculos,
        'vehiculo_seleccionado': vehiculo_seleccionado,
        'tipos_reparacion': tipos_reparacion
    })

def generar_pdf_presupuesto(request, vehiculo_id, tipo):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    reparaciones = HistorialReparacion.objects.filter(vehiculo=vehiculo, tipo_reparacion=tipo).order_by('fecha')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Presupuesto_{vehiculo.placa}_{tipo}.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Presupuesto - {tipo}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Vehículo: {vehiculo.marca} {vehiculo.modelo} ({vehiculo.placa})")
    c.drawString(50, height - 100, f"Cliente: {vehiculo.nombre_cliente}")

    y = height - 140
    total_general = Decimal('0.00')

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Fecha")
    c.drawString(150, y, "Descripción")
    c.drawString(400, y, "Piezas")
    c.drawString(470, y, "Mano de Obra")
    c.drawString(550, y, "Total")
    c.setFont("Helvetica", 12)
    y -= 20

    for r in reparaciones:
        c.drawString(50, y, r.fecha.strftime("%Y-%m-%d"))
        c.drawString(150, y, r.descripcion_trabajo[:40])
        c.drawString(400, y, f"${r.costo_piezas:.2f}")
        c.drawString(470, y, f"${r.costo_mano_obra:.2f}")
        c.drawString(550, y, f"${r.costo_total:.2f}")
        total_general += r.costo_total
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y-10, "TOTAL GENERAL:")
    c.drawString(550, y-10, f"${total_general:.2f}")

    c.save()
    return response