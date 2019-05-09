from django.shortcuts import render
from django.views.generic import View

from django.utils import timezone
from .utils import *


class HomePage(View):

    def get(self, request):
        today = timezone.now()
        yearly_expenses = get_yearly_expenses(year=today.year)
        monthly_expenses = get_monthly_expenses(year=today.year, month=today.month)
        ctx = {
            'yearly_expenses': yearly_expenses,
            'monthly_expenses': monthly_expenses
        }
        return render(request, 'dashboard/index.html', context=ctx)
