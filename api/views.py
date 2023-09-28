from datetime import date, timedelta
from time import time

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from api.config import NO_ROBOTS_MESSAGE
from api.serializers import OrderSerializer, RobotSerializer
from api.utils import create_report_sheet
from orders.models import Order
from robots.models import Robot


class RobotViewSet(ModelViewSet):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        model = request.data['model']
        version = request.data['version']
        request.data['serial'] = f'{model}-{version}'
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def download_report(self, request):
        # Получаем количество роботов за последнюю неделю
        robots = list(self.get_robots_stats(7))
        if not robots:
            return JsonResponse(
                {'message': NO_ROBOTS_MESSAGE}
            )
        report = create_report_sheet(robots)
        response = HttpResponse(
            content_type='application/vnd.ms-excel'
        )
        report.save(response)
        response['Content-Disposition'] = \
            f'attachment; filename="report_{int(time())}.xlsx"'
        return response

    def get_robots_stats(self, days):
        last_week = date.today() - timedelta(days=days)
        return Robot.objects.filter(created__gte=last_week).values(
            'model',
            'version'
        ).annotate(count=Count('id'))


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.data.get('customer_id'))
