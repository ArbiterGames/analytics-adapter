import json
from decimal import Decimal
from datetime import datetime

from django.http import HttpResponse

from input.models import Record
from adapter.utils import Logger
logger = Logger()

DAYS_IN_A_WEEK = 7
TODAY = datetime.today()
BEGINNING_OF_LAST_WEEK = '%s-%s-%s' % (TODAY.year, TODAY.month - 1, TODAY.day - 7)
END_OF_LAST_WEEK = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 1)
BEGINNING_OF_WEEK_BEFORE_LAST = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 14)
END_OF_WEEK_BEFORE_LAST = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 8)


def geckoboard_dau(request):
    response = {'item': []}
    last_week = Record.objects.filter(date__range=(BEGINNING_OF_LAST_WEEK, END_OF_LAST_WEEK))
    last_week_mean = calculate_mean_dau_from_qs(qs=last_week)
    response['item'].append({'value': '{0:.2f}'.format(last_week_mean)})
    week_before_last = Record.objects.filter(date__range=(BEGINNING_OF_WEEK_BEFORE_LAST, END_OF_WEEK_BEFORE_LAST))
    week_before_last_mean = calculate_mean_dau_from_qs(qs=week_before_last)
    response['item'].append({'value': '{0:.2f}'.format(week_before_last_mean)})
    return HttpResponse(json.dumps(response), content_type="application/json")


def geckoboard_revenue(request):
    response = {'item': []}
    last_week = Record.objects.filter(date__range=(BEGINNING_OF_LAST_WEEK, END_OF_LAST_WEEK))
    last_week_mean = calculate_mean_revenue_from_qs(qs=last_week)
    response['item'].append({'value': '{0:.2f}'.format(last_week_mean)})
    week_before_last = Record.objects.filter(date__range=(BEGINNING_OF_WEEK_BEFORE_LAST, END_OF_WEEK_BEFORE_LAST))
    week_before_last_mean = calculate_mean_revenue_from_qs(qs=week_before_last)
    response['item'].append({'value': '{0:.2f}'.format(week_before_last_mean)})
    return HttpResponse(json.dumps(response), content_type="application/json")


def geckoboard_arpu(request):
    response = {'item': []}
    last_week = Record.objects.filter(date__range=(BEGINNING_OF_LAST_WEEK, END_OF_LAST_WEEK))
    last_week_mean = calculate_mean_arpu_from_qs(qs=last_week)
    response['item'].append({'value': '{0:.2f}'.format(last_week_mean)})
    week_before_last = Record.objects.filter(date__range=(BEGINNING_OF_WEEK_BEFORE_LAST, END_OF_WEEK_BEFORE_LAST))
    week_before_last_mean = calculate_mean_arpu_from_qs(qs=week_before_last)
    response['item'].append({'value': '{0:.2f}'.format(week_before_last_mean)})
    return HttpResponse(json.dumps(response), content_type="application/json")


def calculate_mean_dau_from_qs(qs=None):
    try:
        total_dau = sum(Decimal(r.dau) for r in qs.iterator())
        return total_dau / DAYS_IN_A_WEEK
    except Exception as err:
        logger.debug('calculate_mean_dau_from_qs error: %s' % err)
        return Decimal('0')


def calculate_mean_revenue_from_qs(qs=None):
    try:
        total_revenue = sum(Decimal(r.revenue) for r in qs.iterator())
        return total_revenue / DAYS_IN_A_WEEK
    except Exception as err:
        logger.debug('calculate_mean_revenue_from_qs error: %s' % err)
        return Decimal('0')


def calculate_mean_arpu_from_qs(qs=None):
    try:
        mean_revenue = calculate_mean_revenue_from_qs(qs=qs)
        mean_dau = calculate_mean_dau_from_qs(qs=qs)
        return mean_revenue / mean_dau
    except Exception as err:
        logger.debug('calculate_mean_arpu_from_qs error: %s' % err)
        return Decimal('0')
