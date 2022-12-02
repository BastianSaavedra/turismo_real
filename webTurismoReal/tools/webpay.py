import requests
import json
import random
from django.conf import settings
from home.models import *
from tools import utilities

def crearTransaccion(reserva_id, user_id, total, url_webpay):

    # reserva = Reserva.objects.filter(id=reserva_id)
    #
    #
    # try:
    #     order = Reserva.objects.filter(id=reserva_id).get()
    # except Reserva.DoesNotExist:
    #     order = Reserva.objects.create(
    #         guest=users_id,
    #         total_reserva  = total,
    #         huespedes = huespedes,
    #         check_in = checkin,
    #         check_out = checkout,
    #         tour = tour,
    #         detalle_tp = traslado,
    #     )

    try:
        order = BookingOrder.objects.filter(reserva_id=reserva_id).get()
    except BookingOrder.DoesNotExist:
        order = BookingOrder.objects.create(
            reserva_id = reserva_id,
            user = user_id,
            total = total
        )


    buy_order = f"orden{order.id}"
    session_id = str(random.randrange(1000000, 999999999))
    amount = total
    ruta = f"{settings.BASE_URL}{url_webpay}"
    endpoint = settings.WEBPAY_URL
    payload = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": ruta
    }
    booking_headers = {
        'content-type': 'application/json',
        'Tbk-Api-Key-Id': settings.WEBPAY_ID,
        'Tbk-Api-Key-Secret': settings.WEBPAY_SECRET
    }
    response = requests.post(
        endpoint,
        json = payload,
        headers = booking_headers 
    )

    answer = json.loads(response.text)
    BookingOrder.objects.filter(id=order.id).update(token_ws=answer['token'])
    ruta = f"{ answer['url'] }{ answer['token'] }"
    return answer


def crearTransaccionFuncionario(reserva_id, user_id, total, url_webpay):

    # reserva = Reserva.objects.filter(id=reserva_id)
    #
    #
    # try:
    #     order = Reserva.objects.filter(id=reserva_id).get()
    # except Reserva.DoesNotExist:
    #     order = Reserva.objects.create(
    #         guest=users_id,
    #         total_reserva  = total,
    #         huespedes = huespedes,
    #         check_in = checkin,
    #         check_out = checkout,
    #         tour = tour,
    #         detalle_tp = traslado,
    #     )

    try:
        order = BookingOrder.objects.filter(reserva_id=reserva_id).get()
    except BookingOrder.DoesNotExist:
        order = BookingOrder.objects.create(
            reserva_id = reserva_id,
            user = user_id,
            total = total
        )


    buy_order = f"orden{order.id}"
    session_id = str(random.randrange(1000000, 999999999))
    amount = total
    ruta = f"{settings.BASE_URL_MOVIL}{url_webpay}"
    endpoint = settings.WEBPAY_URL
    payload = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": ruta
    }
    booking_headers = {
        'content-type': 'application/json',
        'Tbk-Api-Key-Id': settings.WEBPAY_ID,
        'Tbk-Api-Key-Secret': settings.WEBPAY_SECRET
    }
    response = requests.post(
        endpoint,
        json = payload,
        headers = booking_headers 
    )

    answer = json.loads(response.text)
    BookingOrder.objects.filter(id=order.id).update(token_ws=answer['token'])
    ruta = f"{ answer['url'] }{ answer['token'] }"
    return answer

def verificarTransaccion(token):
    endpoint = f"{settings.WEBPAY_URL}/{token}"
    booking_headers = {
        'content-type': 'application/json',
        'Tbk-Api-Key-Id': settings.WEBPAY_ID,
        'Tbk-Api-Key-Secret': settings.WEBPAY_SECRET
    }
    response = requests.put(endpoint, headers=booking_headers)
    answer = json.loads(response.text)
    if response.status_code == 200:
        return [
            answer['status'],
            answer['card_detail']['card_number'],
            answer['transaction_date']
        ]
    else:
        return ['vacio']


