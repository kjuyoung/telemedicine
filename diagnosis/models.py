from django.db import models

from doctor.models import Doctor
from patient.models import Patient


class DiagnosisRequest(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    request_time = models.DateTimeField()
    desired_diagnosis_time = models.DateTimeField()
    expiration_accept_time = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.patient + ' - ' + self.doctor

    class Meta:
        db_table = "diagnosis_request"
        verbose_name = '진료요청'
