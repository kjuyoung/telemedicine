from django.db import models


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    hospital_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'doctor'
        verbose_name = '의사'


class BusinessHours(models.Model):
    DAY_CHOICES = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, related_name='businesshours')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    lunch_start = models.TimeField(null=True, blank=True)
    lunch_end = models.TimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    class Meta:
        db_table = 'business_hours'
        verbose_name = '영업시간'


class Diagnosis(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=30)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='diagnosis')

    def __str__(self):
        return self.department

    class Meta:
        db_table = "diagnosis_department"
        verbose_name = '진료과'


class UninsuredServices(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=30)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='uninsuredservices')

    def __str__(self):
        return self.department

    class Meta:
        db_table = 'uninsured_services'
        verbose_name = '비급여진료과목'
