from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict
from geoportal_delrio.models import Barrio, Cliente, Ruta
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

def update_barrio(d: dict):
    """
    Actualiza un barrio validando que la nueva geometría sea válida y no se solape.
    """
    try:
        cur = connection.cursor()
        # 1. Ajuste a la rejilla de precisión
        query_snap = "SELECT ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)"
        cur.execute(query_snap, [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        # 2. Validar geometría con GEOS
        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {"ok": False, "message": "Geometría inválida", "data": None}

        # 3. Comprobar solapamiento excluyendo el registro actual (id != %s)
        # Se usa el nombre de tabla "d.barrios" definido en el modelo
        query_overlap = """
            SELECT id FROM "d.barrios" 
            WHERE ST_Relate(geom, %s, 'T********') AND id != %s
        """
        cur.execute(query_overlap, [snapped_wkb, d['id']])
        if len(cur.fetchall()) > 0:
            return {"ok": False, "message": "El polígono intersecta con otros barrios", "data": None}

        # 4. Actualizar mediante el ORM[cite: 11]
        obj = Barrio.objects.get(id=d['id'])
        obj.nombre = d.get('nombre', obj.nombre)
        obj.codigo = d.get('codigo', obj.codigo)
        obj.distrito = d.get('distrito', obj.distrito)
        obj.area = g.area
        obj.numero_clientes = d.get('numero_clientes', obj.numero_clientes)
        obj.geom = g
        obj.save()

        return {
            "ok": True, 
            "message": "Datos actualizados correctamente", 
            "data": [model_to_dict(obj)]
        }
    except Barrio.DoesNotExist:
        return {"ok": False, "message": "El barrio no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}

def update_cliente(d: dict):
    """
    Actualiza un cliente validando que el nuevo punto esté dentro de un barrio[cite: 5].
    """
    try:
        cur = connection.cursor()
        # 1. Ajuste a la rejilla[cite: 5]
        query_snap = "SELECT ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)"
        cur.execute(query_snap, [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        # 2. Validar geometría[cite: 5]
        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {"ok": False, "message": "Geometría inválida", "data": None}

        # 3. Comprobar si el punto sigue estando dentro de un barrio[cite: 5]
        query_within = 'SELECT id FROM "d.barrios" WHERE ST_Within(%s, geom)'
        cur.execute(query_within, [snapped_wkb])
        if len(cur.fetchall()) == 0:
            return {"ok": False, "message": "El punto está fuera de cualquier barrio", "data": None}

        # 4. Actualizar mediante el ORM[cite: 11]
        obj = Cliente.objects.get(id=d['id'])
        obj.nombre = d.get('nombre', obj.nombre)
        obj.direccion = d.get('direccion', obj.direccion)
        obj.telefono = d.get('telefono', obj.telefono)
        obj.tipo_cliente = d.get('tipo_cliente', obj.tipo_cliente)
        obj.barrio = d.get('barrio', obj.barrio)
        obj.geom = g
        obj.save()

        return {
            "ok": True, 
            "message": "Datos actualizados correctamente", 
            "data": [model_to_dict(obj)]
        }
    except Cliente.DoesNotExist:
        return {"ok": False, "message": "El cliente no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}

def update_ruta(d: dict):
    """
    Actualiza una ruta validando que no intersecte con otras líneas existentes[cite: 8].
    """
    try:
        cur = connection.cursor()
        # 1. Ajuste a la rejilla[cite: 8]
        query_snap = "SELECT ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)"
        cur.execute(query_snap, [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb = cur.fetchall()[0][0]

        # 2. Validar geometría[cite: 8]
        g = GEOSGeometry(snapped_wkb, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {"ok": False, "message": "Geometría inválida", "data": None}

        # 3. Comprobar intersecciones excluyendo la ruta actual[cite: 8]
        query_inter = 'SELECT id FROM "d.rutas" WHERE ST_Intersects(geom, %s) AND id != %s'
        cur.execute(query_inter, [snapped_wkb, d['id']])
        if len(cur.fetchall()) > 0:
            return {"ok": False, "message": "La línea intersecta con otras rutas", "data": None}

        # 4. Actualizar mediante el ORM[cite: 11]
        obj = Ruta.objects.get(id=d['id'])
        obj.distancia = d.get('distancia', obj.distancia)
        obj.tiempo = d.get('tiempo', obj.tiempo)
        obj.estado = d.get('estado', obj.estado)
        obj.barrio_destino = d.get('barrio_destino', obj.barrio_destino)
        obj.numero_paradas = d.get('numero_paradas', obj.numero_paradas)
        obj.geom = g
        obj.save()

        return {
            "ok": True, 
            "message": "Datos actualizados correctamente", 
            "data": [model_to_dict(obj)]
        }
    except Ruta.DoesNotExist:
        return {"ok": False, "message": "La ruta no existe", "data": None}
    except Exception as e:
        return {"ok": False, "message": str(e), "data": None}