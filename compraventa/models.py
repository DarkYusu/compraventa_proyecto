from django.db import models

# Create your models here.

class Vehiculo(models.Model):
    patente = models.CharField(max_length=6, unique=True, primary_key=True)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    year = models.IntegerField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente}) - Estado: {self.activo}"

class Chofer(models.Model):
    rut = models.CharField(max_length=9, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    activo = models.BooleanField(default=False)
    creacion_registro = models.DateField(auto_now_add=True)
    vehiculo = models.ForeignKey(Vehiculo, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"

class RegistroContabilidad(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_compra = models.DateField(null=False)
    valor = models.FloatField(null=False)
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, to_field='patente', unique=True)

    def __str__(self):
        return f"Registro {self.id} - {self.vehiculo.patente} - {self.fecha_compra}"
