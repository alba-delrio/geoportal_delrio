from django.test import TestCase, Client

class GeoportalCompletoTests(TestCase):
    def setUp(self):
        """Configuración inicial: se ejecuta antes de cada test individual."""
        self.client = Client()
        
        # Payload base para un Barrio (necesario para probar Clientes)
        self.barrio_payload = {
            'nombre': 'Barrio Test',
            'codigo': 'T001',
            'geom': 'POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'
        }
        # Insertamos el barrio inicial
        self.client.post('/geoportal_delrio/barrios/', data=self.barrio_payload)

    # --- TESTS DE BARRIOS ---
    def test_barrio_operaciones(self):
        """Prueba Ver todos, Ver uno y Borrar para Barrios"""
        # Select All
        res_all = self.client.get('/geoportal_delrio/barrios/')
        self.assertEqual(res_all.status_code, 200)
        
        # Select One
        res_one = self.client.get('/geoportal_delrio/barrios/1/')
        self.assertEqual(res_one.status_code, 200)
        
        # Delete (POST a la URL /delete/)
        res_del = self.client.post('/geoportal_delrio/barrios/1/delete/')
        self.assertTrue(res_del.json()['ok'])

    # --- TESTS DE CLIENTES (Validación ST_Within) ---
    def test_cliente_dentro_fuera_barrio(self):
        """Prueba la lógica espacial de inserción de clientes"""
        
        # CASO 1: Cliente DENTRO (Debe funcionar)
        payload_ok = {
            'nombre': 'Juan Dentro',
            'direccion': 'Calle A',
            'geom': 'POINT(5 5)'
        }
        res_ok = self.client.post('/geoportal_delrio/clientes/', data=payload_ok)
        self.assertTrue(res_ok.json()['ok'])

        # CASO 2: Cliente FUERA (Debe fallar)
        payload_error = {
            'nombre': 'Pedro Fuera',
            'direccion': 'Calle B',
            'geom': 'POINT(20 20)'
        }
        res_error = self.client.post('/geoportal_delrio/clientes/', data=payload_error)
        self.assertFalse(res_error.json()['ok'])

    # --- TESTS DE RUTAS (Validación ST_Intersects) ---
    def test_ruta_no_cruce(self):
        """Prueba que no se permitan rutas que se crucen"""
        
        # 1. Ruta base horizontal
        ruta_base = {
            'distancia': 10.0,
            'tiempo': 15,
            'estado': 'Activa',
            'numero_paradas': 2,
            'geom': 'LINESTRING(0 5, 10 5)'
        }
        self.client.post('/geoportal_delrio/rutas/', data=ruta_base)

        # 2. Ruta vertical que cruza (Debe fallar)
        ruta_cruce = {
            'distancia': 10.0,
            'tiempo': 20,
            'estado': 'Activa',
            'numero_paradas': 2,
            'geom': 'LINESTRING(5 0, 5 10)'
        }
        res_cruce = self.client.post('/geoportal_delrio/rutas/', data=ruta_cruce)
        self.assertFalse(res_cruce.json()['ok'])

    def test_actualizar_ruta(self):
        """Prueba el POST a la URL de ID para actualizar"""
        payload_upd = {
            'estado': 'Mantenimiento',
            'geom': 'LINESTRING(0 0, 1 1)' 
        }
        res = self.client.post('/geoportal_delrio/rutas/1/', data=payload_upd)
        self.assertEqual(res.status_code, 200)