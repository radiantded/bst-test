from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import OrderViewSet, RobotViewSet


router_v1 = DefaultRouter()
router_v1.register('robots', RobotViewSet)
router_v1.register('orders', OrderViewSet)

urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
]
