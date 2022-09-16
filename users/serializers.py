from rest_framework import serializers
from users.models import Employees

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employees 
        fields=('id','first_name','last_name','company_name','city','state','zip','email','web','age')
        read_only_fields = ['id','company_name','city','state','zip','email','web']