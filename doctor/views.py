from datetime import datetime

from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from doctor.models import Doctor, Diagnosis, UninsuredServices, BusinessHours
from doctor.serializers import DoctorSerializer, BusinessHoursSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request):
        diagnosis_data = request.data.pop('diagnosis_department')
        uninsured_services_data = request.data.pop('uninsured_services_department')
        business_hours_data = request.data.pop('business_hours')

        doctor_serializer = DoctorSerializer(data=request.data)

        if doctor_serializer.is_valid():
            doctor = doctor_serializer.save()

            for department in diagnosis_data:
                Diagnosis.objects.create(doctor=doctor, department=department)

            for department in uninsured_services_data:
                UninsuredServices.objects.create(doctor=doctor, department=department)

            for business_hour in business_hours_data:
                business_hour_serializer = BusinessHoursSerializer(data=business_hour)
                if business_hour_serializer.is_valid():
                    BusinessHours.objects.create(doctor=doctor, **business_hour_serializer.validated_data)
                else:
                    return Response(business_hour_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(doctor_serializer.errors)
            return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        hospital_name = request.query_params.get('hospital_name', None)
        diagnosis_department = request.query_params.get('diagnosis_department', None)
        uninsured_services_department = request.query_params.get('uninsured_services_department', None)
        datetime_str = request.query_params.get('desired_diagnosis_time', None)
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M") if datetime_str else None

        queryset = self.get_queryset().prefetch_related('diagnosis', 'uninsuredservices', 'businesshours')

        query = Q()

        if name is not None:
            query &= Q(name__icontains=name)
        if hospital_name is not None:
            query &= Q(hospital_name__icontains=hospital_name)
        if diagnosis_department is not None:
            query &= Q(diagnosis__department__icontains=diagnosis_department)
        if uninsured_services_department is not None:
            query &= Q(uninsuredservices__department__icontains=uninsured_services_department)
        if datetime_obj is not None:
            weekday = datetime_obj.strftime('%a').lower()
            query &= Q(businesshours__day=weekday, businesshours__opening_time__lte=datetime_obj.time(),
                       businesshours__closing_time__gte=datetime_obj.time(), businesshours__closed=False)

        queryset = queryset.filter(query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
