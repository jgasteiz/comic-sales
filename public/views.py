from django.shortcuts import render
from django.utils import timezone

from comixology.models import Sale


def sale_list(request):
    today = timezone.datetime.today().date()
    context = {
        'sale_list': Sale.objects.filter(date_end__gte=today)
    }
    return render(request, 'public/sale_list.html', context=context)
