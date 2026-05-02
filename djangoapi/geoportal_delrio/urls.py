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
    # --- RUTAS DINÁMICAS (Estilo Profesor) ---
    
    # Para operaciones sin ID (ej: selectall, insert)
    # URL en Postman: .../barrios/selectall/  o  .../barrios/insert/
    path('barrios/<str:action>/', views.BarriosView.as_view(), name='barrios_views'),
    path('clientes/<str:action>/', views.ClientesView.as_view(), name='clientes_views'),
    path('rutas/<str:action>/', views.RutasView.as_view(), name='rutas_views'),

    # Para operaciones con ID (ej: selectone, update, delete)
    # URL en Postman: .../barrios/selectone/1/  o  .../barrios/delete/1/
    path('barrios/<str:action>/<int:id>/', views.BarriosView.as_view(), name='barrios_views_id'),
    path('clientes/<str:action>/<int:id>/', views.ClientesView.as_view(), name='clientes_views_id'),
    path('rutas/<str:action>/<int:id>/', views.RutasView.as_view(), name='rutas_views_id'),
]



# urlpatterns = [
#     # --- BARRIOS ---
#     path('barrios/', 
#          views.BarriosView.as_view(actions={'GET': 'selectall', 'POST': 'insert'}), 
#          name='B_GET_selectall()_POST_insert()'), 
    
#     path('barrios/<int:id>/', 
#          views.BarriosView.as_view(actions={'GET': 'selectone', 'POST': 'update'}), 
#          name='B_GET_selectone(id)_POST_update(id)'),
    
#     path('barrios/<int:id>/delete/', 
#          views.BarriosView.as_view(actions={'POST': 'delete'}), 
#          name='B_POST_delete(id)'),

#     # --- CLIENTES ---
#     path('clientes/', 
#          views.ClientesView.as_view(actions={'GET': 'selectall', 'POST': 'insert'}), 
#          name='C_GET_selectall()_POST_insert()'),
    
#     path('clientes/<int:id>/', 
#          views.ClientesView.as_view(actions={'GET': 'selectone', 'POST': 'update'}), 
#          name='C_GET_selectone(id)_POST_update(id)'),
    
#     path('clientes/<int:id>/delete/', 
#          views.ClientesView.as_view(actions={'POST': 'delete'}), 
#          name='C_POST_delete(id)'),

#     # --- RUTAS ---
#     path('rutas/', 
#          views.RutasView.as_view(actions={'GET': 'selectall', 'POST': 'insert'}), 
#          name='R_GET_selectall()_POST_insert()'),
    
#     path('rutas/<int:id>/', 
#          views.RutasView.as_view(actions={'GET': 'selectone', 'POST': 'update'}), 
#          name='R_GET_selectone(id)_POST_update(id)'),
    
#     path('rutas/<int:id>/delete/', 
#          views.RutasView.as_view(actions={'POST': 'delete'}), 
#          name='R_POST_delete(id)'),
# ]


# urlpatterns = [
#     # --- BARRIOS ---
#     path('barrios/', views.BarriosView.as_view(), name='B_GET_selectall()_POST_insert()'), 
#     path('barrios/<int:id>/', views.BarriosView.as_view(), name='B_GET_selectone(id)_POST_update(id)'),
#     path('barrios/<int:id>/delete/', views.BarriosView.as_view(), name='B_POST_delete(id)'),

#     # --- CLIENTES ---
#     path('clientes/', views.ClientesView.as_view(), name='C_GET_selectall()_POST_insert()'),
#     path('clientes/<int:id>/', views.ClientesView.as_view(), name='C_GET_selectone(id)_POST_update(id)'),
#     path('clientes/<int:id>/delete/', views.ClientesView.as_view(), name='C_POST_delete(id)'),

#     # --- RUTAS ---
#     path('rutas/', views.RutasView.as_view(), name='R_GET_selectall()_POST_insert()'),
#     path('rutas/<int:id>/', views.RutasView.as_view(), name='R_GET_selectone(id)_POST_update(id)'),
#     path('rutas/<int:id>/delete/', views.RutasView.as_view(), name='R_POST_delete(id)'),
# ]



# urlpatterns = [
#     # Ruta de prueba
#     path('hello/', views.HelloGeoportal_DelRio.as_view(), name='hello_geoportal'),

#     # --- RUTAS PARA BARRIOS ---
#     # GET: listar todos | POST: insertar nuevo
#     path('barrios/', views.BarriosView.as_view({
#         'get': 'selectall', 
#         'post': 'insert'
#     })),
#     # GET: ver uno | POST: actualizar datos
#     path('barrios/<int:id>/', views.BarriosView.as_view({
#         'get': 'selectone', 
#         'post': 'update'
#     })),
#     # POST: borrar
#     path('barrios/<int:id>/delete/', views.BarriosView.as_view({
#         'post': 'delete'
#     })),

#     # --- RUTAS PARA CLIENTES ---
#     path('clientes/', views.ClientesView.as_view({
#         'get': 'selectall', 
#         'post': 'insert'
#     })),
    
#     path('clientes/<int:id>/', views.ClientesView.as_view({
#         'get': 'selectone', 
#         'post': 'update'
#     })),
    
#     path('clientes/<int:id>/delete/', views.ClientesView.as_view({
#         'post': 'delete'
#     })),

#     # --- RUTAS PARA RUTAS ---
#     path('rutas/', views.RutasView.as_view({
#         'get': 'selectall', 
#         'post': 'insert'
#     })),
    
#     path('rutas/<int:id>/', views.RutasView.as_view({
#         'get': 'selectone', 
#         'post': 'update'
#     })),
    
#     path('rutas/<int:id>/delete/', views.RutasView.as_view({
#         'post': 'delete'
#     })),
# ]