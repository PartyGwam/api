import os
from pyfcm import FCMNotification

api_key = os.environ['PG_FCM_SERVER_KEY']
push_service = FCMNotification(api_key=api_key)


def send_push_to_single_user(user, title, body):
    return push_service.notify_single_device(
        registration_id=user,
        message_title=title,
        message_body=body
    )


def send_push_to_multiple_user(users, title, body):
    if type(users) != 'list':
        raise TypeError('유저 토큰들을 리스트로 제공해 주세요')

    return push_service.notify_multiple_devices(
        registration_ids=users,
        message_title=title,
        message_body=body
    )
