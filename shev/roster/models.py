from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.timezone import utc

from shev.roster.exceptions import (ShiftsOverlapError, DayNearNightError,
    ShiftLacksTypeError, ShiftLacksDayError, ShiftLacksTimeError,
    MultipleAnnualLeaveError)


class BaseManager(models.Manager):
    def create(self, **kwargs):
        instance = self.model(**kwargs)
        instance.full_clean()
        instance.save()
        return instance


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def create(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        instance.full_clean()
        instance.save()
        return instance

    @property
    def admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse('admin:{}_{}_change'.format(content_type.app_label, content_type.model), args=(self.pk,))


class TeamOrAgency(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name_plural = "Teams and Agencies"

    label = models.CharField(max_length=40)

    def __unicode__(self):
        return u"%s" % (self.label)


class Person(BaseModel):
    BAND_7 = "7"
    BANDS = (
        (BAND_7, "7"),
        ("6.5", "6.5"),
        ("6", "6"),
        ("5", "5"),
        ("4", "4"),
        ("2", "2"),
    )

    class Meta(BaseModel.Meta):
        verbose_name_plural = "People"

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    band = models.CharField(max_length=5, choices=BANDS)
    team_or_agency = models.ForeignKey(TeamOrAgency)
## TODO
# Person needs a 'pod' and an ALEntitlement field?
#
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class ShiftType(BaseModel):
    SHIFT_LONG = "LONG"
    SHIFT_EARLY = "EARLY"
    SHIFT_LATE = "LATE"
    SHIFT_NIGHT = "NIGHT"
    SHIFT_CHOICES = (
        (SHIFT_LONG, "Long day"),
        (SHIFT_EARLY, "Early"),
        (SHIFT_LATE, "Late"),
        (SHIFT_NIGHT, "Night"),
    )
    label = models.CharField(max_length=40)
    hours = models.DecimalField(null=True, max_digits=6, decimal_places=2)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    mutex = models.BooleanField(default=True, editable=False)
    clinical = models.BooleanField()
    supernumeraryable = models.BooleanField(default=False)  # sorry for the name
    time_of_day = models.CharField(null=True, max_length=10, choices=SHIFT_CHOICES, blank=True)

    def __unicode__(self):
        return u"%s:%s hours" % (self.label, self.hours)


class Outcome(BaseModel):
    OUTCOME_SICK = "SICK"
    OUTCOME_CANCELLED = "CANCELLED"
    OUTCOME_SELF_CANCELLED = "SELF_CANCELLED"
    OUTCOME_ABSENT = "ABSENT"
    OUTCOME_MAYBE_BACK = "MAYBE_BACK"
    OUTCOME_IS_BACK = "IS_BACK"
    OUTCOMES = (
        (OUTCOME_SICK, "Sick"),
        (OUTCOME_CANCELLED, "Cancelled"),
        (OUTCOME_SELF_CANCELLED, "Self Cancelled"),
        (OUTCOME_ABSENT, "Absent"),
        (OUTCOME_MAYBE_BACK, "?back"),
        (OUTCOME_IS_BACK, "Is back"),
    )
    label = models.CharField(null=True, max_length=100, choices=OUTCOMES)

    def __unicode__(self):
        return u"%s" % (self.label)


class Day(BaseModel):
    day = models.DateField(unique=True)
    note = models.TextField(default='', blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.day, self.note)

    def get_absolute_url(self):
        return reverse('day', kwargs={'year': self.day.year, 'month': self.day.month, 'day': self.day.day})

    def clinical_shifts(self):
        return self.shifts.prefetch_related('shift_type').filter(shift_type__clinical=True)

    @property
    def previous_day(self):
        day, _ = Day.objects.get_or_create(day=self.day - timedelta(days=1))
        return day

    @property
    def next_day(self):
        day, _ = Day.objects.get_or_create(day=self.day + timedelta(days=1))
        return day


class ShiftManager(BaseManager):
    pass


class Shift(BaseModel):
    @classmethod
    def make_datetime(cls, date_value, time_value):
        date_time = datetime(year=date_value.year, month=date_value.month, day=date_value.day,
            hour=time_value.hour, minute=time_value.minute).replace(tzinfo=utc)
        return date_time

    objects = ShiftManager()

    REGULAR_CONTRACT = "REGU"
    CONTRACTS = (
        (REGULAR_CONTRACT, "Regular"),
        ("BNKL", "Bank Line"),
        ("BANK", "Bank"),
        ("AGNL", "Agency Line"),
        ("AGNC", "Agency"),
    )

    day = models.ForeignKey(Day, related_name='shifts')
    person = models.ForeignKey(Person, related_name='shifts')
    shift_type = models.ForeignKey(ShiftType, related_name='shifts')
    supernumerary = models.BooleanField(default=False)
    # start, end and hours maybe blank but not null, if null on save,
    # will be filled with their shift_type values
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    hours = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)
    contract = models.CharField(max_length=4, choices=CONTRACTS, default=REGULAR_CONTRACT)
    outcome = models.ForeignKey(Outcome, null=True, blank=True)
    note = models.CharField(max_length=80, null=True, blank=True)
    assigned = models.CharField(max_length=20, null=True, blank=True) # this is something to do with the pod...

    def __unicode__(self):
        return u"%s - %s - %s - %s hours" % (self.day.day, self.person, self.shift_type.label, self.hours)

    def clean_fields(self, *args, **kwargs):
        super(Shift, self).clean_fields(*args, **kwargs)
        self.errored = False
        try:
            exclude = set(kwargs.get('exclude', [])) & set(['shift_type', 'day', 'person'])
            if exclude:
                self.errored = True
                return
            else:
                if self.hours is None:
                    self.hours = self.shift_type.hours
                for field in ['start', 'end']:
                    if getattr(self, field) is None:
                        time_value = getattr(self.shift_type, field)
                        if time_value is None:
                            if self.shift_type.clinical:
                                raise ShiftLacksTimeError(params={'field': field})
                        else:
                            date_time = Shift.make_datetime(self.day.day, time_value)
                            setattr(self, field, date_time)
        except Exception:
            self.errored = True
            raise

    def clean(self, *args, **kwargs):
        super(Shift, self).clean(*args, **kwargs)
        if self.errored:
            return

        other_shifts = (self.person.shifts.exclude(pk=self.pk)
            .prefetch_related('shift_type'))
        if self.shift_type.mutex:
            other_shifts = other_shifts.exclude(shift_type__mutex=False)
            ExceptionClass = ShiftsOverlapError
        else:
            # We assume we only have annual leave, this data model smells
            other_shifts = other_shifts.exclude(shift_type__mutex=True)
            ExceptionClass = MultipleAnnualLeaveError

        if self.start is not None:
            other_shifts = other_shifts.exclude(end__lte=self.start).exclude(end__isnull=True)
        if self.end is not None:
            other_shifts = other_shifts.exclude(start__gte=self.end).exclude(start__isnull=True)
        other_shifts = other_shifts.values_list('id', flat=True)
        if other_shifts:
            raise ExceptionClass(params={'shift_ids': other_shifts})

        if self.shift_type.mutex:
            time_of_day = self.shift_type.time_of_day
            if time_of_day and time_of_day == ShiftType.SHIFT_NIGHT:
                # check there's not a day shift following or preceeding
                day_shifts = (self.person.shifts.prefetch_related('shift_type', 'day')
                    .exclude(shift_type__time_of_day=None)
                    .exclude(shift_type__time_of_day=ShiftType.SHIFT_NIGHT)
                    .filter(Q(day__day=self.day.day) | Q(day__day=self.day.day + timedelta(1)))
                    .values_list('id', flat=True))
                if day_shifts:
                    raise DayNearNightError(params={'shift_ids': day_shifts})

            if time_of_day and time_of_day != ShiftType.SHIFT_NIGHT:
                # check there's not a night shift following or preceeding
                night_shifts = (self.person.shifts.prefetch_related('shift_type', 'day')
                    .filter(shift_type__time_of_day=ShiftType.SHIFT_NIGHT)
                    .filter(Q(day__day=self.day.day) | Q(day__day=self.day.day - timedelta(1)))
                    .values_list('id', flat=True))
                if night_shifts:
                    raise DayNearNightError(params={'shift_ids': night_shifts})

    @property
    def maybe_occuring(self):
        return self.outcome.label == Outcome.OUTCOME_MAYBE_BACK

    @property
    def occuring(self):
        return self.outcome is None or self.outcome.label == Outcome.OUTCOME_IS_BACK

    @property
    def band_type_sup(self):
        # import ipdb; ipdb.set_trace()
        val = self.person.band
        val = self.contract if self.contract != self.REGULAR_CONTRACT else val
        val = 'Supernumerary' if self.supernumerary else val
        return val
