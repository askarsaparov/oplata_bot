from datetime import datetime
import pytz
from aiogram_forms.errors import ValidationError

from db import select_payments, select_need_payments, update_is_paid


def timestamp_to_datetime(timestamp):
    timestamp = timestamp / 1000
    return datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Tashkent'))


def to_timestamp(str_date):
    dt = datetime.strptime(str_date, '%d.%m.%Y')
    return int(dt.timestamp() * 1000)


def sum_payments():
    sum_payments = 0
    payments = select_payments()
    for payment in payments:
        # print(payment[2])
        sum_payments += payment[2]
    return sum_payments


def get_sum_payments():
    payments = sum_payments()
    payments = f"{payments:,.2f}"
    return payments


def get_duty():
    payments = sum_payments()
    duty = 454167000 - payments
    duty = f"{duty:,.2f}"
    return duty


def get_all_need_payments():
    payments = select_need_payments()
    payments_list = []
    for enum, payment in enumerate(payments):
        payment_list = list(payment)
        payment_list[0] = f"{enum + 1}."
        payment_list[2] = f"{payment_list[2]:,.2f}"
        payment_list.append(to_timestamp(payment_list[1]))
        payments_list.append(payment_list)
    payments_list = sorted(payments_list, key=lambda x: x[4])
    return payments_list


def get_all_payments():
    payments = select_payments()
    payments_list = []
    for enum, payment in enumerate(payments):
        payment_list = list(payment)
        payment_list[0] = f"{enum + 1}."
        payment_list[2] = f"{payment_list[2]:,.2f}"
        payment_list.append(to_timestamp(payment_list[1]))
        payments_list.append(payment_list)
    payments_list = sorted(payments_list, key=lambda x: x[3])
    return payments_list


def validate_date_format(date):
    try:
        datetime.strptime(date, '%d.%m.%Y')
        year = datetime.strptime(date, '%d.%m.%Y').year
        if not (year == 2023 or year == 2024 or year == 2025):
            raise ValidationError('Сəне надурыс киритилди.', code='date_prefix')
    except Exception as e:
        raise ValidationError('Сəне надурыс киритилди.', code='date_prefix')


def validate_amount_format(amount):
    try:
        amount = int(amount)
        if amount < 1:
            raise ValidationError('Толеў муғдары надурыс киритилди.', code='amount_prefix')
    except Exception as e:
        raise ValidationError('Толеў муғдары надурыс киритилди.', code='amount_prefix')


def edit_is_paid():
    sum_payments = get_sum_payments()
    sum_payments = sum_payments[:-3]
    sum_payments = sum_payments.replace(',', '')
    sum_payments = int(sum_payments)
    sum = 0
    for payment in select_need_payments():
        sum += payment[2]
        if sum_payments >= sum and payment[3] != 1:
            update_is_paid(payment[0])


def get_graphic():
    current_date = datetime.now().date()
    month = current_date.month
    year = current_date.year
    day = 14
    graphic = datetime(year, month, day).date()
    if graphic > current_date:
        if graphic.month == 1:
            graphic = graphic.replace(month=12, year=year - 1)
        else:
            graphic = graphic.replace(month=month - 1)
    response = graphic.strftime("%d.%m.%Y")
    return response


# print(get_graphic())

def graphic_payments():
    graphic = get_graphic()
    sum = 0
    need_payments = select_need_payments()
    for payment in need_payments:
        sum += payment[2]
        if payment[1] == graphic:
            break
    return sum


def get_graphic_payments():
    graphic = graphic_payments()
    graphic = f"{graphic:,.2f}"
    return graphic


# print(get_graphic_payments())


def info():
    response = []
    all_payments = get_sum_payments()
    graphic = get_graphic_payments()
    need_payment = sum_payments() - graphic_payments()
    need_payment = f"+{need_payment:,.2f}" if need_payment >= 0 else f"{need_payment:,.2f}"
    duty = get_duty()
    response.append(all_payments)
    response.append(duty)
    response.append(graphic)
    response.append(need_payment)
    return response

# info()
