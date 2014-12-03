import json
import datetime
from decimal import Decimal

from django.http import HttpResponse

from input.models import Record
from adapter.utils import Logger
logger = Logger()

DAYS_IN_A_WEEK = 7
TODAY = datetime.datetime.today()
BEGINNING_OF_LAST_WEEK = (TODAY - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
END_OF_LAST_WEEK = (TODAY - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
BEGINNING_OF_WEEK_BEFORE_LAST = (TODAY - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
END_OF_WEEK_BEFORE_LAST = (TODAY - datetime.timedelta(days=18)).strftime('%Y-%m-%d')


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
            "text": "Monthly Average Temperature"
        },
        "xAxis": {
            "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        },
        "yAxis": {
            "title": {
                "style": {
                    "color": "#b9bbbb"
                },
                "text": "Temperature"
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
        "series": [{
                "color": "#108ec5",
                "name": "NewYork",
                "data": [17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
            }, {
                "color": "#52b238",
                "name": "Berlin",
                "data": [13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
            }, {
                "color": "#ee5728",
                "name": "London",
                "data": [11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
        }]
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
