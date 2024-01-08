# Generated by Django 5.0.1 on 2024-01-08 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30, unique=True)),
                ("hospital_name", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name": "의사",
                "db_table": "mydoctor",
            },
        ),
        migrations.CreateModel(
            name="Diagnosis",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("department", models.CharField(max_length=30)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diagnosis",
                        to="doctor.doctor",
                    ),
                ),
            ],
            options={
                "verbose_name": "진료과",
                "db_table": "diagnosis_department",
            },
        ),
        migrations.CreateModel(
            name="BusinessHours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("mon", "Monday"),
                            ("tue", "Tuesday"),
                            ("wed", "Wednesday"),
                            ("thu", "Thursday"),
                            ("fri", "Friday"),
                            ("sat", "Saturday"),
                            ("sun", "Sunday"),
                        ],
                        max_length=3,
                    ),
                ),
                ("opening_time", models.TimeField(blank=True, null=True)),
                ("closing_time", models.TimeField(blank=True, null=True)),
                ("lunch_start", models.TimeField(blank=True, null=True)),
                ("lunch_end", models.TimeField(blank=True, null=True)),
                ("closed", models.BooleanField(default=False)),
                (
                    "doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="businesshours",
                        to="doctor.doctor",
                    ),
                ),
            ],
            options={
                "verbose_name": "영업시간",
                "db_table": "business_hours",
            },
        ),
        migrations.CreateModel(
            name="UninsuredServices",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("department", models.CharField(max_length=30)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uninsuredservices",
                        to="doctor.doctor",
                    ),
                ),
            ],
            options={
                "verbose_name": "비급여진료과목",
                "db_table": "uninsured_services",
            },
        ),
    ]
