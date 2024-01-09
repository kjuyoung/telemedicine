from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from doctor.models import BusinessHours
from .models import DiagnosisRequest, Patient, Doctor
from datetime import datetime, timedelta


class DiagnosisRequestTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.doctor = Doctor.objects.create(name="Dr. Lee")
        self.patient = Patient.objects.create(name="Patient Kim")

        self.diagnosis_request_data = {
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'desired_diagnosis_time': (datetime.now() + timedelta(days=1)).isoformat(),
        }

        business_hours = [
            {
                "day": "mon",
                "opening_time": "09:00",
                "closing_time": "18:00",
                "lunch_start": "12:00",
                "lunch_end": "13:00",
                "closed": "False"
            },
            {
                "day": "tue",
                "opening_time": "09:00",
                "closing_time": "18:00",
                "lunch_start": "12:00",
                "lunch_end": "13:00",
                "closed": "False"
            },
            {
                "day": "wed",
                "opening_time": "09:00",
                "closing_time": "18:00",
                "lunch_start": "12:00",
                "lunch_end": "13:00",
                "closed": "False"
            },
            {
                "day": "thu",
                "opening_time": "09:00",
                "closing_time": "18:00",
                "lunch_start": "12:00",
                "lunch_end": "13:00",
                "closed": "False"
            },
            {
                "day": "fri",
                "opening_time": "09:00",
                "closing_time": "18:00",
                "lunch_start": "12:00",
                "lunch_end": "13:00",
                "closed": "False"
            },
            {
                "day": "sat",
                "opening_time": None,
                "closing_time": None,
                "lunch_start": None,
                "lunch_end": None,
                "closed": "True"
            },
            {
                "day": "sun",
                "opening_time": None,
                "closing_time": None,
                "lunch_start": None,
                "lunch_end": None,
                "closed": "True"
            },
        ]
        for hours in business_hours:
            BusinessHours.objects.create(doctor=self.doctor, **hours)

    def test_diagnosis_request_creation(self):
        response = self.client.post(reverse('diagnosis'), self.diagnosis_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiagnosisRequest.objects.count(), 1)
        self.assertEqual(DiagnosisRequest.objects.get().patient, self.patient)

    def test_diagnosis_request_list(self):
        DiagnosisRequest.objects.create(patient=self.patient, doctor=self.doctor,
                                        desired_diagnosis_time=datetime.now() + timedelta(days=1),
                                        request_time=datetime.now(),
                                        expiration_accept_time=datetime.now() + timedelta(minutes=10))
        response = self.client.get(reverse('diagnosis'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_diagnosis_request_accept(self):
        diagnosis_request = DiagnosisRequest.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            desired_diagnosis_time=datetime.now() + timedelta(days=1),
            request_time=datetime.now(),
            expiration_accept_time=datetime.now() + timedelta(minutes=10)
        )
        response = self.client.post(reverse('diagnosis-accept', kwargs={'pk': diagnosis_request.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnosis_request.refresh_from_db()
        self.assertEqual(diagnosis_request.is_accepted, True)

