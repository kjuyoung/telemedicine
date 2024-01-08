from django.db import models


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'patient'
        verbose_name = '환자'
