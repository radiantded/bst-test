from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.config import (
    DEFAULT_EMAIL, NOTIFY_MESSAGE, NOTIFY_SUBJECT,
    ORDER_SUCCESS_MESSAGE, ORDER_SUCCESS_SUBJECT
)
from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Order)
def order_post_save_handler(sender, instance, **kwargs):
    # Если робот есть в наличии - отправляем письмо об успешном заказе
    if Robot.objects.filter(
        serial=instance.robot_serial
    ).exists():
        model, version = instance.robot_serial.split('-')
        send_mail(
            subject=ORDER_SUCCESS_SUBJECT,
            from_email=DEFAULT_EMAIL,
            recipient_list=[instance.customer.email],
            message=ORDER_SUCCESS_MESSAGE.format(
                model=model,
                version=version
            )
        )
        # Покупатель не должен получать уведомлений о наличии робота
        instance.is_informed = True
        instance.save()


@receiver(post_save, sender=Robot)
def robot_post_save_handler(sender, instance, **kwargs):
    # Если есть непроинформированные о наличии робота
    # покупатели - отправляем уведомление
    for order in Order.objects.filter(
        robot_serial=instance.serial,
        is_informed=False
    ):
        model, version = order.robot_serial.split('-')
        send_mail(
            subject=NOTIFY_SUBJECT,
            from_email=DEFAULT_EMAIL,
            recipient_list=[order.customer.email],
            message=NOTIFY_MESSAGE.format(
                model=model,
                version=version
            )
        )
        # Пользователь проинформирован
        order.is_informed = True
        order.save()
