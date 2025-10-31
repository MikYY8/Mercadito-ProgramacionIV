from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import comparar_precios

class CompararPrecios(APIView):
    def get(self, request, nombre):
        return Response({"resultado": comparar_precios(nombre)})