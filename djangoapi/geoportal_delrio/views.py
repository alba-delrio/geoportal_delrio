from django.shortcuts import render
from . import models
# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View

from core.myLib.geometryTools import WkbConversor, GeometryChecks
from core.myLib.baseDjangoView import BaseDjangoView

#my code
from geoportal_delrio.operations.insertDjango import insert_barrio, insert_cliente, insert_ruta
from geoportal_delrio.operations.deleteDjango import delete_barrio, delete_cliente, delete_ruta
from geoportal_delrio.operations.selectDjango import select_barrio, selectall_barrios, select_cliente, selectall_clientes, select_ruta, selectall_rutas
from geoportal_delrio.operations.updateDjango import update_barrio, update_cliente, update_ruta

class HelloGeoportal_DelRio(View):
    actions = {}
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Geoportal_DelRio. Hello world", "data":[request.GET.dict()]})
    def post(self, request):
        return JsonResponse({"ok":True,"message": "Geoportal_DelRio. Hello world", "data":[request.POST.dict()]})

############ BARRIOS
class BarriosView(BaseDjangoView, ):
    actions = {}
    #GET OPERATIONS
    def selectone(self, request, id):
        r=select_barrio({'id':id})
        return JsonResponse(r)

    def selectall(self, request):
        r=selectall_barrios()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        d=request.POST.dict()
        r=insert_barrio(d)
        return JsonResponse(r)
    def update(self, request, id):
        d = request.POST.dict()
        d['id'] = id
        r=update_barrio(d)
        return JsonResponse(r)
    def delete(self, request, id):
        d = request.POST.dict()
        d['id'] = id
        r=delete_barrio(d)
        return JsonResponse(r)

############ CLIENTES
class ClientesView(BaseDjangoView, ):
    actions = {}
    #GET OPERATIONS
    def selectone(self, request, id):
        r=select_cliente({'id':id})
        return JsonResponse(r)

    def selectall(self, request):
        r=selectall_clientes()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        d=request.POST.dict()
        r=insert_cliente(d)
        return JsonResponse(r)
    def update(self, request, id):
        d = request.POST.dict()
        d['id'] = id
        r=update_cliente(d)
        return JsonResponse(r)
    def delete(self, request, id):
        d = request.POST.dict()
        d['id'] = id
        r=delete_cliente(d)
        return JsonResponse(r)

############ RUTAS
class RutasView(BaseDjangoView, ):
    actions = {}
    #GET OPERATIONS
    def selectone(self, request, id):
        r=select_ruta({'id':id})
        return JsonResponse(r)

    def selectall(self, request):
        r=selectall_rutas()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        d=request.POST.dict()
        r=insert_ruta(d)
        return JsonResponse(r)
    def update(self, request, id):
        d = request.POST.dict()
        d['id'] = id
        r=update_ruta(d)
        return JsonResponse(r)
    def delete(self, request, id):
        d = request.POST.dict()
        d['id'] = id
        r=delete_ruta(d)
        return JsonResponse(r)