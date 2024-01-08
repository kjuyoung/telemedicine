from rest_framework import serializers

from doctor.models import Diagnosis, UninsuredServices, BusinessHours, Doctor


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ['department']


class UninsuredServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UninsuredServices
        fields = ['department']


class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ['day', 'opening_time', 'closing_time', 'lunch_start', 'lunch_end', 'closed']


class DoctorSerializer(serializers.ModelSerializer):
    diagnosis = DiagnosisSerializer(many=True, read_only=True)
    uninsuredservices = UninsuredServicesSerializer(many=True, read_only=True)
    businesshours = BusinessHoursSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ['name', 'hospital_name', 'diagnosis', 'uninsuredservices', 'businesshours']
