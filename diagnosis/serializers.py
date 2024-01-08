from rest_framework import serializers
from diagnosis.models import DiagnosisRequest


class DiagnosisRequestSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')

    class Meta:
        model = DiagnosisRequest
        fields = ['id', 'patient_name', 'doctor_name', 'desired_diagnosis_time', 'expiration_accept_time']
