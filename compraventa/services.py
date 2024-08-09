from .models import Vehiculo, Chofer, RegistroContabilidad

def crear_vehiculo(patente, marca, modelo, year):
    vehiculo, created = Vehiculo.objects.get_or_create(
        patente=patente,
        defaults={
            'marca': marca,
            'modelo': modelo,
            'year': year,
        }
    )
    if created:
        return vehiculo
    else:
        raise ValueError(f"El vehículo con patente {patente} ya existe.")

def crear_chofer(rut, nombre, apellido, vehiculo_patente, activo=False):
    try:
        vehiculo = Vehiculo.objects.get(patente=vehiculo_patente)
    except Vehiculo.DoesNotExist:
        raise ValueError(f"No se encontró el vehículo con patente {vehiculo_patente}.")

    chofer, created = Chofer.objects.get_or_create(
        rut=rut,
        defaults={
            'nombre': nombre,
            'apellido': apellido,
            'activo': activo,
            'vehiculo': vehiculo,
        }
    )
    if created:
        return chofer
    else:
        raise ValueError(f"El chofer con RUT {rut} ya existe.")

def crear_registro_contable(fecha_compra, valor, vehiculo_patente):
    try:
        vehiculo = Vehiculo.objects.get(patente=vehiculo_patente)
    except Vehiculo.DoesNotExist:
        raise ValueError(f"No se encontró el vehículo con patente {vehiculo_patente}.")

    registro, created = RegistroContabilidad.objects.get_or_create(
        vehiculo=vehiculo,
        defaults={
            'fecha_compra': fecha_compra,
            'valor': valor,
        }
    )
    if created:
        return registro
    else:
        raise ValueError(f"Ya existe un registro contable para el vehículo con patente {vehiculo_patente}.")

def deshabilitar_chofer(rut):
    try:
        chofer = Chofer.objects.get(rut=rut)
        chofer.activo = False
        chofer.save()
        return f"Chofer {chofer.nombre} {chofer.apellido} ({chofer.rut}) ha sido deshabilitado. Estado actual: Activo = {chofer.activo}"
    except Chofer.DoesNotExist:
        raise ValueError(f"No se encontró el chofer con RUT {rut}.")

def deshabilitar_vehiculo(patente):
    try:
        vehiculo = Vehiculo.objects.get(patente=patente)
        vehiculo.activo = False
        vehiculo.save()
        chofer = Chofer.objects.filter(vehiculo=vehiculo).first()
        if chofer:
            chofer.activo = False
            chofer.save()
            return (f"Vehículo {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente}) ha sido deshabilitado. "
                    f"Estado actual del vehículo: Activo = {vehiculo.activo}. "
                    f"Chofer: {chofer.nombre} {chofer.apellido} ({chofer.rut}) - Activo = {chofer.activo}")
        else:
            return f"Vehículo {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente}) ha sido deshabilitado. Estado actual: Activo = {vehiculo.activo}. No hay chofer asignado."
    except Vehiculo.DoesNotExist:
        raise ValueError(f"No se encontró el vehículo con patente {patente}.")


def habilitar_chofer(rut):
    try:
        chofer = Chofer.objects.get(rut=rut)
        chofer.activo = True
        chofer.save()
        return f"Chofer {chofer.nombre} {chofer.apellido} ({chofer.rut}) ha sido habilitado. Estado actual: Activo = {chofer.activo}"
    except Chofer.DoesNotExist:
        raise ValueError(f"No se encontró el chofer con RUT {rut}.")

def habilitar_vehiculo(patente):
    try:
        vehiculo = Vehiculo.objects.get(patente=patente)
        vehiculo.activo = True
        vehiculo.save()
        chofer = Chofer.objects.filter(vehiculo=vehiculo).first()
        if chofer:
            chofer.activo = True
            chofer.save()
            return (f"Vehículo {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente}) ha sido habilitado. "
                    f"Estado actual del vehículo: Activo = {vehiculo.activo}. "
                    f"Chofer: {chofer.nombre} {chofer.apellido} ({chofer.rut}) - Activo = {chofer.activo}")
        else:
            return f"Vehículo {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente}) ha sido habilitado. Estado actual: Activo = {vehiculo.activo}. No hay chofer asignado."
    except Vehiculo.DoesNotExist:
        raise ValueError(f"No se encontró el vehículo con patente {patente}.")

    
def obtener_vehiculo(patente):
    try:
        vehiculo = Vehiculo.objects.get(patente=patente)
        return f"Vehículo: {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente}) - Año: {vehiculo.year}"
    except Vehiculo.DoesNotExist:
        raise ValueError(f"No se encontró el vehículo con patente {patente}.")

def obtener_chofer(rut):
    try:
        chofer = Chofer.objects.get(rut=rut)
        vehiculo = chofer.vehiculo
        return (f"Chofer: {chofer.nombre} {chofer.apellido} ({chofer.rut}) - "
                f"Vehículo asignado: {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente}) - "
                f"Estado activo: {chofer.activo}")
    except Chofer.DoesNotExist:
        raise ValueError(f"No se encontró el chofer con RUT {rut}.")
    
def asignar_chofer_a_vehiculo(rut, patente):
    try:
        chofer = Chofer.objects.get(rut=rut)
        vehiculo = Vehiculo.objects.get(patente=patente)
        if chofer.vehiculo:
            chofer.vehiculo = None
            chofer.save()
        chofer.vehiculo = vehiculo
        chofer.save()
        
        return f"Chofer {chofer.nombre} {chofer.apellido} ({chofer.rut}) ha sido asignado al vehículo {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente})."
    
    except Chofer.DoesNotExist:
        raise ValueError(f"No se encontró el chofer con RUT {rut}.")
    except Vehiculo.DoesNotExist:
        raise ValueError(f"No se encontró el vehículo con patente {patente}.")


def imprimir_datos_vehiculos():
    vehiculos = Vehiculo.objects.all()
    if not vehiculos:
        return "No hay vehículos registrados."
    
    vehiculo_data = []
    for vehiculo in vehiculos:
        chofer = Chofer.objects.filter(vehiculo=vehiculo).first()
        chofer_info = f"{chofer.nombre} {chofer.apellido} ({chofer.rut})" if chofer else "No asignado"
        vehiculo_data.append(
            f"Vehículo: {vehiculo.marca} {vehiculo.modelo} ({vehiculo.patente}) - "
            f"Año: {vehiculo.year} - Activo: {vehiculo.activo} - Chofer: {chofer_info}"
        )
    return "\n".join(vehiculo_data)
