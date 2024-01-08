from django.urls import include, path
from rest_framework import routers

from diagnosis import views

router = routers.DefaultRouter()
router.register('', views.DiagnosisRequestViewSet, basename='diagnosis')

urlpatterns = [
    path('', views.DiagnosisRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='diagnosis'),
    path('<int:doctor_id>/', views.DiagnosisRequestViewSet.as_view({'get': 'list'}), name='diagnosis-list'),
    path('<int:pk>/accept/', views.DiagnosisRequestViewSet.as_view({'post': 'accept'}), name='diagnosis-accept'),
]
