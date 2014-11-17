import json
from decimal import Decimal
from datetime import datetime
from django.http import HttpResponse

from input.models import Record
from adapter.utils import Logger
logger = Logger()


def geckoboard_arpu(request):
    TODAY = datetime.today()
    BEGINNING_OF_LAST_WEEK = '%s-%s-%s' % (TODAY.year, TODAY.month - 1, TODAY.day - 7)
    END_OF_LAST_WEEK = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 1)
    BEGINNING_OF_WEEK_BEFORE_LAST = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 14)
    END_OF_WEEK_BEFORE_LAST = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 8)
    response = {'item': []}

    last_week = Record.objects.filter(date__range=(BEGINNING_OF_LAST_WEEK, END_OF_LAST_WEEK))
    last_week_mean = get_mean_from_qs(qs=last_week)
    response['item'].append({'value': '{0:.2f}'.format(last_week_mean)})

    week_before_last = Record.objects.filter(date__range=(BEGINNING_OF_WEEK_BEFORE_LAST, END_OF_WEEK_BEFORE_LAST))
    week_before_last_mean = get_mean_from_qs(qs=week_before_last)
    response['item'].append({'value': '{0:.2f}'.format(week_before_last_mean)})

    return HttpResponse(json.dumps(response), content_type="application/json")


def get_mean_from_qs(qs=None):
    DAYS_IN_A_WEEK = 7
    try:
        total_dau = 0
        total_revenue = 0
        for i in qs.iterator():
            total_dau += Decimal(i.dau)
            total_revenue += Decimal(i.revenue)
        return total_revenue / total_dau / DAYS_IN_A_WEEK
    except Exception as err:
        logger.debug('get_mean_from_qs error: %s' % err)
        return Decimal('0')
