from django import template
from django.utils import timezone
from time import strftime

register = template.Library()


@register.filter
def to_pounds(pence):
    if not pence:
        return ''
    # endif

    try:
        pence = int(pence)/100
    except ValueError:
        pass
    # end except

    return pence


@register.filter
def monthly_txn_date(start_date):
    now = timezone.now()
    target_date = timezone.datetime(now.year, now.month, start_date.day)
    return target_date.strftime('%d/%m/%Y')


@register.filter
def yearly_txn_date(start_date):
    now = timezone.now()
    target_date = timezone.datetime(now.year, start_date.month, start_date.day)
    return target_date.strftime('%d/%m/%Y')
