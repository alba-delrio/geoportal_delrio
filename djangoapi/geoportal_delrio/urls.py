from django.urls import path
from . import views

'''
http://localhost:8001/geoportal_delrio/

selectall-->GET/(barrios, clientes, rutas)/
selectone-->GET/(barrios, clientes, rutas)/1/

insert-->POST/barrios///nombre:"Barrio Norte"&codigo:"BN01"&geom:"POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))"/
             /clientes///nombre:"Juan Pérez"&direccion:"Calle Falsa 123"&telefono: "555-1234"&tipo_cliente: "Premium"&geom:"POINT(5 5)"/
             /rutas///distancia:15.5&tiempo:30&estado:"Activa"&numero_paradas:5&geom:"LINESTRING(0 0, 5 5, 10 10)"/

update-->POST/barrios/1///nombre:"Barrio Norte Editado"&geom:"POLYGON((0 0, 0 12, 12 12, 12 0, 0 0))"/
             /clientes/10///nombre:"Juan Pérez Actualizado"&geom:"POINT(6 6)"/
             /rutas/100///estado:"Mantenimiento"&geom:"LINESTRING(0 0, 4 4, 11 11)"/

delete-->POST/barrios/1/delete/
             /clientes/10/delete
             /rutas/100/delete

EN EL NAVEGADOR NO SE ESCRIBE GET O POST
EN REALIDAD EN POST LOS DATOS VAN POR DETRÁS (DESPUÉS DE ///) PERO PARA SABER LO QUE LLEVA
'''

urlpatterns = [
    # Ruta de prueba
    path('hello/', views.HelloGeoportal_DelRio.as_view(), name='hello_geoportal'),

    # --- RUTAS PARA BARRIOS ---
    # GET: listar todos | POST: insertar nuevo
    path('barrios/', views.BarriosView.as_view({
        'get': 'selectall', 
        'post': 'insert'
    })),
    # GET: ver uno | POST: actualizar datos
    path('barrios/<int:id>/', views.BarriosView.as_view({
        'get': 'selectone', 
        'post': 'update'
    })),
    # POST: borrar
    path('barrios/<int:id>/delete/', views.BarriosView.as_view({
        'post': 'delete'
    })),

    # --- RUTAS PARA CLIENTES ---
    path('clientes/', views.ClientesView.as_view({
        'get': 'selectall', 
        'post': 'insert'
    })),
    
    path('clientes/<int:id>/', views.ClientesView.as_view({
        'get': 'selectone', 
        'post': 'update'
    })),
    
    path('clientes/<int:id>/delete/', views.ClientesView.as_view({
        'post': 'delete'
    })),

    # --- RUTAS PARA RUTAS ---
    path('rutas/', views.RutasView.as_view({
        'get': 'selectall', 
        'post': 'insert'
    })),
    
    path('rutas/<int:id>/', views.RutasView.as_view({
        'get': 'selectone', 
        'post': 'update'
    })),
    
    path('rutas/<int:id>/delete/', views.RutasView.as_view({
        'post': 'delete'
    })),
]