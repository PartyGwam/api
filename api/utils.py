import os
from pyfcm import FCMNotification

from apps.notifications.models import Notification

api_key = os.environ['PG_FCM_SERVER_KEY']
push_service = FCMNotification(api_key=api_key)


def send_push_to_single_user(user, party, title, body):
    fcm_token = user.user.fcm_token
    Notification.objects.create_notification(party, user, title, body=body)
    return push_service.notify_single_device(
        registration_id=fcm_token,
        message_title=title,
        message_body=body
    )


def send_push_to_multiple_user(users, party, title, body):
    if type(users) is not list:
        raise TypeError('유저 토큰들을 리스트로 제공해 주세요')

    fcm_tokens = [user.user.fcm_token for user in users]
    for user in users:
        Notification.objects.create_notification(party, user, title, body=body)

    return push_service.notify_multiple_devices(
        registration_ids=fcm_tokens,
        message_title=title,
        message_body=body
    )
