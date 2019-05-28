import logging

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from .utils import *


class HomePage(View):

    logger = logging.getLogger(__name__)

    def get(self, request):
        # self.logger.debug("IP Address for debug-toolbar: %s" % request.META['REMOTE_ADDR'])
        today = timezone.now()
        yearly_expenses = get_yearly_expenses(year=today.year)
        monthly_expenses = get_monthly_expenses(year=today.year, month=today.month)
        ctx = {
            'today': today,
            'yearly_expenses': yearly_expenses,
            'monthly_expenses': monthly_expenses
        }
        return render(request, 'dashboard/index.html', context=ctx)
