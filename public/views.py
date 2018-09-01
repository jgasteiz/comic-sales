import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from comixology.models import Sale


def sale_list(request):
    today = timezone.datetime.today().date()
    context = {
        'sale_list': Sale.objects.filter(date_end__gte=today)
    }
    return render(request, 'public/sale_list.html', context=context)


def api_all_sales(request):
    today = timezone.datetime.today().date()
    comic_sales = Sale.objects.filter(date_end__gte=today)
    all_sales = [f"{s.title}, ends on {s.date_end.strftime('%B %d')}" for s in comic_sales]
    return HttpResponse(json.dumps(all_sales), content_type='application/json')


def api_last_sales(request):
    today = timezone.datetime.today().date()
    comic_sales = Sale.objects.filter(date_end__gte=today, created_at__gte=today - datetime.timedelta(days=7))
    last_sales = [f"{s.title}, ends on {s.date_end.strftime('%B %d')}" for s in comic_sales]
    return HttpResponse(json.dumps(last_sales), content_type='application/json')
