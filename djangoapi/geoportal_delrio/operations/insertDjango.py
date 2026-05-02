from django.contrib.gis.geos import GEOSGeometry 
from django.forms.models import model_to_dict
from django.db import connection

# Importamos tus modelos de Django
from geoportal_delrio.models import Barrio, Cliente, Ruta

# Importamos la configuración del proyecto[cite: 7]
from djangoapi.settings import EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION

def insert_barrio(d: dict):
    """Inserta un barrio validando solapamientos de polígonos."""
    try:
        cur = connection.cursor()
        
        # 1. Obtener geometría ajustada y validar validez[cite: 4]
        query_snap = "SELECT ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)"
        cur.execute(query_snap, [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb_geometry = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría de barrio inválida', 'data': None}

        # 2. Comprobar solapamiento de interiores con ST_Relate 'T********'[cite: 4]
        query_overlap = """ 
            SELECT id FROM "d.barrios" WHERE ST_Relate(geom, %s, 'T********')
        """
        cur.execute(query_overlap, [snapped_wkb_geometry])
        if len(cur.fetchall()) > 0:
            return {'ok': False, 'message': 'El barrio intersecta con otros barrios', 'data': None}

        # 3. Guardar con ORM
        d['geom'] = g
        d['area'] = g.area # Cálculo automático del área[cite: 4]
        nuevo_barrio = Barrio(**d)
        nuevo_barrio.save()

        res_dict = model_to_dict(nuevo_barrio)
        res_dict['geom'] = g.wkt
        return {'ok': True, 'message': 'Barrio insertado', 'data': [res_dict]}

    except Exception as e:
        return {'ok': False, 'message': str(e), 'data': None}


def insert_cliente(d: dict):
    """Inserta un cliente validando que esté dentro de un barrio."""
    try:
        cur = connection.cursor()
        
        # 1. Ajustar punto a rejilla[cite: 5]
        query_snap = "SELECT ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)"
        cur.execute(query_snap, [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb_geometry = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Punto de cliente inválido', 'data': None}

        # 2. Comprobar si el punto está dentro de algún barrio con ST_Within[cite: 5]
        query_within = """ 
            SELECT id FROM "d.barrios" WHERE ST_Within(%s, geom)
        """
        cur.execute(query_within, [snapped_wkb_geometry])
        if len(cur.fetchall()) == 0:
            return {'ok': False, 'message': 'El cliente está fuera de cualquier barrio', 'data': None}

        # 3. Guardar con ORM[cite: 11]
        d['geom'] = g
        nuevo_cliente = Cliente(**d)
        nuevo_cliente.save()

        res_dict = model_to_dict(nuevo_cliente)
        res_dict['geom'] = g.wkt
        return {'ok': True, 'message': 'Cliente insertado', 'data': [res_dict]}

    except Exception as e:
        return {'ok': False, 'message': str(e), 'data': None}


def insert_ruta(d: dict):
    """Inserta una ruta validando intersecciones con otras líneas."""
    try:
        cur = connection.cursor()
        
        # 1. Ajustar línea a rejilla[cite: 8]
        query_snap = "SELECT ST_SnapToGrid(ST_GeomFromText(%s, %s), %s)"
        cur.execute(query_snap, [d['geom'], EPSG_FOR_GEOMETRIES, ST_SNAP_PRECISION])
        snapped_wkb_geometry = cur.fetchall()[0][0]

        g = GEOSGeometry(snapped_wkb_geometry, srid=EPSG_FOR_GEOMETRIES)
        if not g.valid:
            return {'ok': False, 'message': 'Línea de ruta inválida', 'data': None}

        # 2. Comprobar si la línea corta otras rutas con ST_Intersects[cite: 8]
        query_intersects = """ 
            SELECT id FROM "d.rutas" WHERE ST_Intersects(geom, %s)
        """
        cur.execute(query_intersects, [snapped_wkb_geometry])
        if len(cur.fetchall()) > 0:
            return {'ok': False, 'message': 'La ruta intersecta con otras rutas', 'data': None}

        # 3. Guardar con ORM[cite: 11]
        d['geom'] = g
        nueva_ruta = Ruta(**d)
        nueva_ruta.save()

        res_dict = model_to_dict(nueva_ruta)
        res_dict['geom'] = g.wkt
        return {'ok': True, 'message': 'Ruta insertada', 'data': [res_dict]}

    except Exception as e:
        return {'ok': False, 'message': str(e), 'data': None}