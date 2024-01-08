from datetime import datetime, timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from diagnosis.models import DiagnosisRequest
from diagnosis.serializers import DiagnosisRequestSerializer
from doctor.models import Doctor
from patient.models import Patient


class DiagnosisRequestViewSet(viewsets.ModelViewSet):
    queryset = DiagnosisRequest.objects.all()
    serializer_class = DiagnosisRequestSerializer

    def list(self, request, *args, **kwargs):
        doctor_id = kwargs.get('doctor_id')
        if doctor_id is not None:
            self.queryset = self.queryset.filter(doctor_id=doctor_id, is_accepted=False)

        response = super().list(request, *args, **kwargs)
        for i, data in enumerate(response.data):
            request_info = {
                'id': data['id'],
                'patient_name': data['patient_name'],
                'desired_diagnosis_time': data['desired_diagnosis_time'],
                'expiration_accept_time': data['expiration_accept_time']
            }
            response.data[i] = request_info

        return Response(response.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def accept(self, request):
        diagnosis_request = self.get_object()
        diagnosis_request.is_accepted = True
        diagnosis_request.save()

        response_data = {
            'id': diagnosis_request.id,
            'patient_name': diagnosis_request.patient.name,
            'desired_diagnosis_time': diagnosis_request.desired_diagnosis_time,
            'expiration_accept_time': diagnosis_request.expiration_accept_time
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')
        doctor_id = request.data.get('doctor_id')
        desired_diagnosis_time = request.data.get('desired_diagnosis_time')

        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)

        request_time = datetime.now()
        expiration_accept_time = self.calculate_expiration_time(request_time, doctor)

        diagnosis_request = DiagnosisRequest(
            patient=patient,
            doctor=doctor,
            request_time=request_time,
            desired_diagnosis_time=desired_diagnosis_time,
            expiration_accept_time=expiration_accept_time,
        )
        diagnosis_request.save()

        serializer = self.get_serializer(diagnosis_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def calculate_expiration_time(request_time, doctor):
        day_dict = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}

        expiration_time = request_time + timedelta(minutes=20)

        businesshours = doctor.businesshours.filter(day=day_dict[request_time.weekday()]).first()

        if businesshours is None or businesshours.closed:
            while True:
                expiration_time += timedelta(days=1)
                businesshours = doctor.businesshours.filter(day=day_dict[expiration_time.weekday()]).first()
                if businesshours is not None and not businesshours.closed:
                    break

        expiration_time = DiagnosisRequestViewSet.set_expiration_based_on_opening_time(businesshours.opening_time, expiration_time)

        if expiration_time.time() >= businesshours.closing_time:
            expiration_time = DiagnosisRequestViewSet.set_expiration_based_on_opening_time(businesshours.opening_time, expiration_time)
            expiration_time += timedelta(days=1)

            if businesshours.closed:
                while True:
                    expiration_time += timedelta(days=1)
                    businesshours = doctor.businesshours.get(day=day_dict[expiration_time.weekday()])
                    if not businesshours.closed:
                        break

        elif businesshours.lunch_start <= expiration_time.time() <= businesshours.lunch_end:
            expiration_time = DiagnosisRequestViewSet.set_expiration_based_on_lunch_time(businesshours.lunch_end, expiration_time)

        return expiration_time

    @staticmethod
    def set_expiration_based_on_opening_time(opening_time, expiration_time):
        expiration_time = expiration_time.replace(
            hour=opening_time.hour,
            minute=opening_time.minute,
            second=opening_time.second,
            microsecond=0
        )
        expiration_time += timedelta(minutes=15)
        return expiration_time

    @staticmethod
    def set_expiration_based_on_lunch_time(lunch_end, expiration_time):
        expiration_time = expiration_time.replace(
            hour=lunch_end.hour,
            minute=lunch_end.minute,
            second=lunch_end.second,
            microsecond=0
        )
        expiration_time += timedelta(minutes=15)
        return expiration_time
