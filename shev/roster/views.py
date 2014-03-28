from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone

from . import models


def home(request):
    return HttpResponseRedirect(reverse('overview'))


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
    return render_to_response("overview.html", {'days': days, 'bands': models.Person.BANDS})


def day(request, day, month, year):
    the_day = get_object_or_404(models.Day, day = datetime(int(year),int(month),int(day)))
    the_shifts = the_day.clinical_shifts().prefetch_related('outcome').prefetch_related('person')
    day_shifts = []
    night_shifts = []
    non_shifts = []
    for shift in the_shifts:
        if shift.occuring or shift.maybe_occuring:
            if shift.shift_type.time_of_day != models.ShiftType.SHIFT_NIGHT:
                day_shifts.append(shift)
            else:
                night_shifts.append(shift)
        else:
            non_shifts.append(shift)
    context = {
        'day': the_day,
        'shifts': the_shifts,
        'day_shifts': day_shifts,
        'night_shifts': night_shifts,
        'non_shifts': non_shifts,
    }
    return render_to_response("day.html", context)


def person(request, pkid):
    person = models.Person.objects.get(id=pkid)
    return render_to_response("person.html", {"person": person})
