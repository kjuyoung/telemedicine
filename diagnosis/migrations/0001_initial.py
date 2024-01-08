# Generated by Django 5.0.1 on 2024-01-08 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("doctor", "0001_initial"),
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiagnosisRequest",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("request_time", models.DateTimeField()),
                ("desired_diagnosis_time", models.DateTimeField()),
                ("expiration_accept_time", models.DateTimeField()),
                ("is_accepted", models.BooleanField(default=False)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="patient.patient",
                    ),
                ),
            ],
            options={
                "verbose_name": "진료요청",
                "db_table": "diagnosis_request",
            },
        ),
    ]