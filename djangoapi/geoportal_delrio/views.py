from django.shortcuts import render
from . import models
# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View

from core.myLib.geometryTools import WkbConversor, GeometryChecks
from core.myLib.baseDjangoView import BaseDjangoView
from django.contrib.auth.mixins import LoginRequiredMixin
#my code
from geoportal_delrio.operations.insertDjango import insert_barrio, insert_cliente, insert_ruta
from geoportal_delrio.operations.deleteDjango import delete_barrio, delete_cliente, delete_ruta
from geoportal_delrio.operations.selectDjango import select_barrio, selectall_barrios, select_cliente, selectall_clientes, select_ruta, selectall_rutas
from geoportal_delrio.operations.updateDjango import update_barrio, update_cliente, update_ruta

class HelloGeoportal_DelRio(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Geoportal_DelRio. Hello world", "data":[request.GET.dict()]})
    def post(self, request):
        return JsonResponse({"ok":True,"message": "Geoportal_DelRio. Hello world", "data":[request.POST.dict()]})

############ BARRIOS
class BarriosView(BaseDjangoView, ):
    #GET OPERATIONS
    def selectone(self, id):
        r=select_barrio({'id':id})
        return JsonResponse(r)

    def selectall(self):
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
        if r.get('ok') and r.get('data'):
            for item in r['data']:
                # Si 'geom' es un objeto de base de datos, lo pasamos a texto (WKT)
                if 'geom' in item and not isinstance(item['geom'], str):
                    item['geom'] = item['geom'].wkt
        
        return JsonResponse(r)
    # def delete(self, request, id):
    #     d = request.POST.dict()
    #     d['id'] = id
    #     r=delete_barrio(d)
    #     return JsonResponse(r)
    def delete(self, id):
        d = {'id': id}
        r = delete_barrio(d)
        return JsonResponse(r)

############ CLIENTES
class ClientesView(BaseDjangoView, ):
    #GET OPERATIONS
    def selectone(self, id):
        r=select_cliente({'id':id})
        return JsonResponse(r)

    def selectall(self):
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
        if r.get('ok') and r.get('data'):
            for item in r['data']:
                # Si 'geom' es un objeto de base de datos, lo pasamos a texto (WKT)
                if 'geom' in item and not isinstance(item['geom'], str):
                    item['geom'] = item['geom'].wkt
        
        return JsonResponse(r)
    # def delete(self, request, id):
    #     d = request.POST.dict()
    #     d['id'] = id
    #     r=delete_cliente(d)
    #     return JsonResponse(r)
    def delete(self, id):
        d = {'id': id}
        r = delete_cliente(d)
        return JsonResponse(r)

############ RUTAS
class RutasView(BaseDjangoView, ):
    #GET OPERATIONS
    def selectone(self, id):
        r=select_ruta({'id':id})
        return JsonResponse(r)

    def selectall(self):
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
        if r.get('ok') and r.get('data'):
            for item in r['data']:
                # Si 'geom' es un objeto de base de datos, lo pasamos a texto (WKT)
                if 'geom' in item and not isinstance(item['geom'], str):
                    item['geom'] = item['geom'].wkt
        
        return JsonResponse(r)
    # def delete(self, request, id):
    #     d = request.POST.dict()
    #     d['id'] = id
    #     r=delete_ruta(d)
    #     return JsonResponse(r)
    def delete(self, id):
        d = {'id': id}
        r = delete_ruta(d)
        return JsonResponse(r)
    
######USUARIOS##########
class LoginView(View):
    def post(self, request, *args, **kwargs):
# The request object has the user information
        if request.user.is_authenticated:
            username=request.user.username
            return JsonResponse({"ok":"true","message": "The user {0} already is authenticated".format(username), "data":[]})
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)#introduce into the request cookies the session_id, and in the auth_sessions the session data.This way,in followoing requests, know who is the user and if
    # he is already authenticated.
    # The coockies are sent in the response header on POST requests
            return JsonResponse({"ok":"true","message": "User {0} logged in".format(username), "data":[{"userame":username}]})
        else:
    # To make thinks difficult to hackers, you make a random delay,# between 0 and 1 second
            seconds=random.uniform(0, 1)
            time.sleep(seconds)
            return JsonResponse({"ok":"false","message": "Wrong user or password", "data":[]})
        

class LogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username=request.user.username
        logout(request) #removes from the header of the request
                        #the the session_id, stored in a cookie
        return JsonResponse({"ok":"true","message": "The user {0} is now logged out".format(username), "data":[]})
    

class IsLoggedInView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username=request.user.username
            return JsonResponse({"ok":"true","message": "The user {0} is authenticated".format(username), "data":[{"username":username}]})
        else:
            return JsonResponse({"ok":"false","message": "User is no authenticated", "data":[]})





