from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone

from . import models


def home(request):
    return HttpResponse('<h1>Hello World</h1>')

def about(request):
    return HttpResponse("<h1>Whatchew talking about?</h1>")

def overview(request):
    now = timezone.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))
    day = int(request.GET.get('day', now.day))
    start = datetime(year, month, day)
    days = (models.Day.objects
        .filter(day__gte=start, day__lte=start+timedelta(days=7*4))
        .prefetch_related('shifts').select_related('shift__shift_type'))
    return render_to_response("overview.html",{'days': days})

def day(request, day, month, year):
    the_day = get_object_or_404(models.Day, day = datetime(int(year),int(month),int(day)))
    the_shifts = the_day.shifts.all()
    return render_to_response("day.html",{'day': the_day, 'shifts': the_shifts})
