from django.urls import path, include
from rest_framework import routers

from doctor import views

router = routers.DefaultRouter()
router.register('', views.DoctorViewSet)

urlpatterns = [
    path('', include(router.urls))
]
