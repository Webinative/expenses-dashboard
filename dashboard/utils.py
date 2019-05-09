import calendar

from django.db.models import Q
from django.utils import timezone

from .models import Expense, ExpenseFrequency


def get_yearly_expenses(year=None):
    if year is None:
        year = timezone.now().year
    # endif

    start_date = timezone.datetime(year, 1, 1)
    end_date = timezone.datetime(year, 12, 31)

    try:
        frequency = ExpenseFrequency.objects.get(handle='YEARLY')
        return Expense.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=end_date),
            Q(start_date__lte=start_date) | Q(start_date__year=year),
            frequency=frequency
        ).order_by('start_date__month', 'start_date__day')
    except ExpenseFrequency.DoesNotExist:
        print('ExpenseFrequency "YEARLY" does not exist')
        return []


def get_monthly_expenses(year=None, month=None):
    if year is None:
        year = timezone.now().year
    # endif

    if month is None:
        month = timezone.now().month
    # endif

    weekday, num_days = calendar.monthrange(year, month)
    start_date = timezone.datetime(year, month, 1).date()
    end_date = timezone.datetime(year, month, num_days).date()

    try:
        frequency = ExpenseFrequency.objects.get(handle='MONTHLY')
        return Expense.objects.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=end_date),
            start_date__lte=start_date,
            frequency=frequency
        ).order_by('start_date__day')
    except ExpenseFrequency.DoesNotExist:
        print('ExpenseFrequency "MONTHLY" does not exist')
        return []
