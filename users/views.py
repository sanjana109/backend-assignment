from functools import partial
from django.shortcuts import render
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response

from rest_framework.pagination import (PageNumberPagination,LimitOffsetPagination)
from rest_framework import generics

from rest_framework import filters

from users.models import Employees
from users.serializers import EmployeeSerializer

from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET','POST'])
def employeeApi(request):
    if request.method == 'GET':
        employee=Employees.objects.all()
        employees_serializer=EmployeeSerializer(employee,many=True)
        return Response(employees_serializer.data)
    
    elif request.method=='POST':
        employee_data=request.data
        employees_serializer=EmployeeSerializer(data=employee_data, many=True)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return Response(employees_serializer.data)
        return Response(employees_serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET','DELETE','PUT'])
def employeeApiUser(request, id=0):
    if request.method == 'GET':
        print (id)
        if(int(id)>0):
            employee=Employees.objects.filter(pk=id)
            employees_serializer=EmployeeSerializer(employee,many=True)
            return Response(employees_serializer.data)
    elif request.method == 'PUT': 
        employee_data=request.data
        print(id)
        employee=Employees.objects.get(id=id)
        employees_serializer=EmployeeSerializer(employee,data=employee_data, partial=True)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return Response(employees_serializer.data)
        return Response(employees_serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

    elif request.method=='DELETE':
        employee=Employees.objects.get(id=id)
        print(employee)
        employee.delete()
        return Response(status=status.HTTP_200_OK)
 
class EmployeePagination(PageNumberPagination, LimitOffsetPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10000
    page_query_param = 'page'
    default_limit = 5
    limit_query_param = 'l'
    max_limit = 50

class EmployeeAPIView(generics.ListCreateAPIView):
    search_fields = ['first_name','last_name']
    ordering_fields = ['id','age']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination
    




