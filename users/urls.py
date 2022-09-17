from django.urls import re_path
from users import (views,)

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path('api/users$',views.employeeApi),
    re_path('api/users/([0-9]+)$',views.employeeApiUser),
    
    re_path('api/users/scan$', views.EmployeeAPIView.as_view())
]