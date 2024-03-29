import json
import datetime
import random

from decimal import Decimal

from django.http import HttpResponse

from input.models import Record
from input.models import AlgorithmRecord
from adapter.utils import Logger
logger = Logger()

DAYS_IN_A_WEEK = 7
TODAY = datetime.datetime.today()
YESTERDAY = (TODAY - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
BEGINNING_OF_LAST_WEEK = (TODAY - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
END_OF_LAST_WEEK = (TODAY - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
BEGINNING_OF_WEEK_BEFORE_LAST = (TODAY - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
END_OF_WEEK_BEFORE_LAST = (TODAY - datetime.timedelta(days=18)).strftime('%Y-%m-%d')
THIRTY_DAYS_AGO = (TODAY - datetime.timedelta(days=30)).strftime('%Y-%m-%d')


def yesterday(request):
    """ Returns yesterdays metrics that we pull for the daily summary email updates
        regarding overall health of the arbiter server
    """
    record = Record.objects.all().latest('date')
    response = {
        'dau': record.dau,
        'arpu': record.arpu
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


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


def geckoboard_total_revenue(request):
    response = {'item': []}
    last_week = Record.objects.filter(date__range=(BEGINNING_OF_LAST_WEEK, END_OF_LAST_WEEK))
    last_week_total = calculate_total_revenue_from_qs(qs=last_week)
    response['item'].append({'value': '{0:.2f}'.format(last_week_total)})
    week_before_last = Record.objects.filter(date__range=(BEGINNING_OF_WEEK_BEFORE_LAST, END_OF_WEEK_BEFORE_LAST))
    week_before_last_total = calculate_total_revenue_from_qs(qs=week_before_last)
    response['item'].append({'value': '{0:.2f}'.format(week_before_last_total)})
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


def geckoboard_pool_impact(request):
    response = {'item': []}
    last_week = Record.objects.filter(date__range=(BEGINNING_OF_LAST_WEEK, END_OF_LAST_WEEK))
    last_week_mean = calculate_total_pool_impact_from_qs(qs=last_week)
    response['item'].append({'value': '{0:.2f}'.format(last_week_mean / 100)})
    week_before_last = Record.objects.filter(date__range=(BEGINNING_OF_WEEK_BEFORE_LAST, END_OF_WEEK_BEFORE_LAST))
    week_before_last_mean = calculate_total_pool_impact_from_qs(qs=week_before_last)
    response['item'].append({'value': '{0:.2f}'.format(week_before_last_mean / 100)})
    return HttpResponse(json.dumps(response), content_type="application/json")


def geckoboard_algorithm_arpu(request):
    short_days = []
    long_days = []
    chart_data = []
    alg_values = {}
    records_for_past_month = AlgorithmRecord.objects.filter(date__range=(THIRTY_DAYS_AGO, YESTERDAY))
    days_ago = 1
    for record in records_for_past_month:
        alg_values[record.version] = []
        short_days.append((TODAY - datetime.timedelta(days=days_ago)).strftime('%d'))
        long_days.append((TODAY - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d'))
        days_ago += 1

    short_days.reverse()

    for date in long_days:
        for version in alg_values:
            try:
                alg_rec = records_for_past_month.get(version=version, date=date)
                value = float('{0:.2f}'.format(Decimal(alg_rec.value) / Decimal(alg_rec.record.dau)))
            except:
                value = float(0.0)
            alg_values[version].insert(0, value)

    for version in alg_values:
        chart_data.append({
            'color': create_random_hex_color(),
            'name': version,
            'data': alg_values[version]
        })

    response = {
        "chart": {
            "style": {
                "color": "#b9bbbb"
            },
            "renderTo": "container",
            "backgroundColor": "transparent",
            "lineColor": "rgba(35,37,38,100)",
            "plotShadow": False
        },
        "credits": {
            "enabled": False
        },
        "title": {
            "style": {
                "color": "#b9bbbb"
            },
            "text": "Cash Challenge Algorithm"
        },
        "xAxis": {
            "categories": short_days
        },
        "yAxis": {
            "title": {
                "style": {
                    "color": "#b9bbbb"
                },
                "text": "ARPU / DAU in USD"
            }
        },
        "legend": {
            "itemStyle": {
                "color": "#b9bbbb"
            },
            "layout": "vertical",
            "align": "right",
            "verticalAlign": "middle",
            "borderWidth": 0
        },
        "series": chart_data
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


def calculate_mean_dau_from_qs(qs=None):
    try:
        total_dau = sum(Decimal(r.dau) for r in qs.iterator())
        return total_dau / DAYS_IN_A_WEEK
    except Exception as err:
        logger.debug('calculate_mean_dau_from_qs error: %s' % err)
        return Decimal('0')


def calculate_total_revenue_from_qs(qs=None):
    try:
        return sum(Decimal(r.revenue) for r in qs.iterator())
    except Exception as err:
        logger.debug('calculate_total_revenue_from_qs error: %s' % err)
        return Decimal('0')


def calculate_mean_revenue_from_qs(qs=None):
    try:
        total_revenue = sum(Decimal(r.revenue) for r in qs.iterator())
        return total_revenue / DAYS_IN_A_WEEK
    except Exception as err:
        logger.debug('calculate_mean_revenue_from_qs error: %s' % err)
        return Decimal('0')


def calculate_total_pool_impact_from_qs(qs=None):
    try:
        return sum(Decimal(r.prize_pool_impact) for r in qs.iterator())
    except Exception as err:
        logger.debug('calculate_total_pool_impact_from_qs error: %s' % err)
        return Decimal('0')


def calculate_mean_arpu_from_qs(qs=None):
    try:
        mean_revenue = calculate_mean_revenue_from_qs(qs=qs)
        mean_dau = calculate_mean_dau_from_qs(qs=qs)
        return mean_revenue / mean_dau
    except Exception as err:
        logger.debug('calculate_mean_arpu_from_qs error: %s' % err)
        return Decimal('0')


def create_random_hex_color():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())
