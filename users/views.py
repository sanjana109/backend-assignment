from functools import partial

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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

@api_view(['GET','POST','DELETE','PUT'])
def employeeApi(request, id=0):
        
    if request.method == 'GET':
        print (id)
        if(int(id)>0):
           
            employee=Employees.objects.filter(pk=id)
            
            employees_serializer=EmployeeSerializer(employee,many=True)
            return JsonResponse(employees_serializer.data,safe=False)
        else:
            employee=Employees.objects.all()
            #print(employee[0])
            employees_serializer=EmployeeSerializer(employee,many=True)
            return JsonResponse(employees_serializer.data,safe=False)
    
    elif request.method=='POST':
        employee_data=JSONParser().parse(request)
        employees_serializer=EmployeeSerializer(data=employee_data, many=True)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Inserted Successfully",safe=False)
        return Response(employees_serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'PUT': 
        employee_data=JSONParser().parse(request)
        print(id)
        employee=Employees.objects.get(id=id)
        employees_serializer=EmployeeSerializer(employee,data=employee_data, partial=True)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update",safe=False) 

    elif request.method=='DELETE':
        employee=Employees.objects.get(id=id)
        print(employee)
        employee.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def SaveFile(request):
    file=request.FILES['file']
    file_name=default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False) 
 
class EmployeePagination(PageNumberPagination, LimitOffsetPagination):
    #page_size = 10
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
    




