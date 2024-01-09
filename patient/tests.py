from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer


class PatientModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient = Patient.objects.create(name="Patient Kim")

    def test_patient_create(self):
        response = self.client.post(reverse('patient-list'), {
            'name': 'Patient Lee'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_list(self):
        response = self.client.get(reverse('patient-list'))
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_detail(self):
        response = self.client.get(reverse('patient-detail', kwargs={'pk': self.patient.id}))
        patient = Patient.objects.get(id=self.patient.id)
        serializer = PatientSerializer(patient)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
