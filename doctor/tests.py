import json

from django.test import TestCase
from rest_framework.test import APIClient
from .models import Doctor, BusinessHours, Diagnosis, UninsuredServices
from datetime import time


class DoctorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.doctor = Doctor.objects.create(name="Dr. Kim", hospital_name="Seoul Hospital")
        self.business_hours = BusinessHours.objects.create(doctor=self.doctor, day="mon", opening_time=time(hour=9), closing_time=time(hour=18))
        self.diagnosis = Diagnosis.objects.create(doctor=self.doctor, department="Internal Medicine")
        self.uninsured_services = UninsuredServices.objects.create(doctor=self.doctor, department="Cosmetic Surgery")

    def test_doctor_create(self):
        response = self.client.post('/doctor/', json.dumps({
            'name': 'Dr. Park',
            'hospital_name': 'Busan Hospital',
            'diagnosis_department': ['Surgery', 'Internal Medicine'],
            'uninsured_services_department': ['Orthodontics', 'Cosmetic Surgery'],
            'business_hours': [
                {
                    'day': 'tue',
                    'opening_time': '09:00:00',
                    'closing_time': '18:00:00',
                    'lunch_start': None,
                    'lunch_end': None,
                    'closed': False
                }
            ]
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_doctor_list(self):
        response = self.client.get('/doctor/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Dr. Kim')

    def test_doctor_detail(self):
        response = self.client.get(f'/doctor/{self.doctor.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Dr. Kim')
        self.assertEqual(response.data['hospital_name'], 'Seoul Hospital')
