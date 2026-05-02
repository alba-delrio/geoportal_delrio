from django.forms.models import model_to_dict
from geoportal_delrio.models import Barrio, Cliente, Ruta

# --- OPERACIONES PARA BARRIOS ---

def select_barrio(d: dict):
    """Reemplaza selectAsDicts de barriosOOP[cite: 4]."""
    try:
        obj = Barrio.objects.get(id=d['id'])
        data = model_to_dict(obj)
        # Convertimos la geometría a texto WKT para que sea legible en el JSON[cite: 4]
        data['geom'] = obj.geom.wkt if obj.geom else None
        return {"ok": True, "message": "Barrio recuperado", "data": [data]}
    except Barrio.DoesNotExist:
        return {"ok": False, "message": "El barrio no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}

def selectall_barrios():
    """Nueva función para obtener todos los barrios."""
    try:
        objs = Barrio.objects.all()
        data = []
        for obj in objs:
            item = model_to_dict(obj)
            item['geom'] = obj.geom.wkt if obj.geom else None
            data.append(item)
        return {"ok": True, "message": "Lista de barrios", "data": data}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}


# --- OPERACIONES PARA CLIENTES ---

def select_cliente(d: dict):
    """Reemplaza selectAsDicts de clientesOOP[cite: 5]."""
    try:
        obj = Cliente.objects.get(id=d['id'])
        data = model_to_dict(obj)
        data['geom'] = obj.geom.wkt if obj.geom else None
        return {"ok": True, "message": "Cliente recuperado", "data": [data]}
    except Cliente.DoesNotExist:
        return {"ok": False, "message": "El cliente no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}

def selectall_clientes():
    """Nueva función para obtener todos los clientes."""
    try:
        objs = Cliente.objects.all()
        data = []
        for obj in objs:
            item = model_to_dict(obj)
            item['geom'] = obj.geom.wkt if obj.geom else None
            data.append(item)
        return {"ok": True, "message": "Lista de clientes", "data": data}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}


# --- OPERACIONES PARA RUTAS ---

def select_ruta(d: dict):
    """Reemplaza selectAsDicts de rutasOOP[cite: 8]."""
    try:
        obj = Ruta.objects.get(id=d['id'])
        data = model_to_dict(obj)
        data['geom'] = obj.geom.wkt if obj.geom else None
        return {"ok": True, "message": "Ruta recuperada", "data": [data]}
    except Ruta.DoesNotExist:
        return {"ok": False, "message": "La ruta no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}

def selectall_rutas():
    """Nueva función para obtener todas las rutas."""
    try:
        objs = Ruta.objects.all()
        data = []
        for obj in objs:
            item = model_to_dict(obj)
            item['geom'] = obj.geom.wkt if obj.geom else None
            data.append(item)
        return {"ok": True, "message": "Lista de rutas", "data": data}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}