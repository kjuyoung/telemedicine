from django.urls import include, path
from rest_framework import routers

from diagnosis import views

router = routers.DefaultRouter()
router.register('', views.DiagnosisRequestViewSet)

urlpatterns = [
    path('', include(router.urls))
]