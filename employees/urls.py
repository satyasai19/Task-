from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet,  CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('emp/', include(router.urls)),
]


