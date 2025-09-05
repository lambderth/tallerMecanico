from django.db import models

class Vehiculo(models.Model):
    nombre_cliente = models.CharField(max_length=200)
    telefono_cliente = models.CharField(max_length=20, blank=True, null=True)
    email_cliente = models.EmailField(blank=True, null=True)

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.IntegerField("Año")
    placa = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa}) - {self.nombre_cliente}"


class HistorialReparacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="historiales")
    tipo_reparacion = models.CharField(max_length=200)
    descripcion_trabajo = models.TextField()
    costo_piezas = models.DecimalField(max_digits=10, decimal_places=2)
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    @property
    def costo_total(self):
        return self.costo_piezas + self.costo_mano_obra

    def __str__(self):
        return f"{self.vehiculo} - {self.tipo_reparacion} ({self.fecha})"
