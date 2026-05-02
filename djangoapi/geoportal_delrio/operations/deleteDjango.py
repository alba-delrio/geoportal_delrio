from geoportal_delrio.models import Barrio, Cliente, Ruta

def delete_barrio(d: dict):
    """
    Elimina un barrio por ID siguiendo la lógica de barriosOOP[cite: 4].
    """
    try:
        # Intentamos obtener el objeto por su ID[cite: 4, 11]
        obj = Barrio.objects.get(id=d['id'])
        obj.delete()  # Django ejecuta el DELETE en la tabla "d.barrios"
        
        return {
            "ok": True, 
            "message": "Datos eliminados correctamente", 
            "data": [{"rows_deleted": 1}]
        }
    except Barrio.DoesNotExist:
        return {"ok": False, "message": "El barrio con ese ID no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}

def delete_cliente(d: dict):
    """
    Elimina un cliente por ID siguiendo la lógica de clientesOOP[cite: 5].
    """
    try:
        obj = Cliente.objects.get(id=d['id'])
        obj.delete()  # Django ejecuta el DELETE en la tabla "d.clientes"[cite: 11]
        
        return {
            "ok": True, 
            "message": "Datos eliminados correctamente", 
            "data": [{"rows_deleted": 1}]
        }
    except Cliente.DoesNotExist:
        return {"ok": False, "message": "El cliente con ese ID no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}

def delete_ruta(d: dict):
    """
    Elimina una ruta por ID siguiendo la lógica de rutasOOP[cite: 8].
    """
    try:
        obj = Ruta.objects.get(id=d['id'])
        obj.delete()  # Django ejecuta el DELETE en la tabla "d.rutas"[cite: 11]
        
        return {
            "ok": True, 
            "message": "Datos eliminados correctamente", 
            "data": [{"rows_deleted": 1}]
        }
    except Ruta.DoesNotExist:
        return {"ok": False, "message": "La ruta con ese ID no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}