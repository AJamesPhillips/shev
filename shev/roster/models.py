from django.forms import ModelForm
from django.db import models

from shev.roster.exceptions import ShiftsOverlapError


class BaseManager(models.Manager):
    def create(self, **kwargs):
        instance = self.model(**kwargs)
        instance.full_clean()
        instance = super(BaseManager, self).create(**kwargs)
        return instance
        # form = instance.__class__.get_form_class()(instance=instance)
        # if form.is_valid():
        #     return instance


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def create(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        instance.full_clean()
        instance = super(BaseModel, cls).create(*args, **kwargs)
        return instance
        # form = cls.get_form_class()(instance=instance)
        # if form.is_valid():
        #     return instance

    # @classmethod
    # def get_form_class(cls):
    #     raise NotImplementedError('Subclasses should implement this')


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
    mutex = models.BooleanField(default=True)
    clinical = models.BooleanField()
    supernumeraryable = models.BooleanField(default=False)  # sorry for the name
    time_of_day = models.CharField(null=True, max_length=10, choices=SHIFT_CHOICES)

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
    day = models.DateField()
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.day, self.note)


class ShiftManager(BaseManager):
    pass


class Shift(BaseModel):

    # @classmethod
    # def get_form_class(cls):
    #     return ShiftForm

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
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    hours = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)
    contract = models.CharField(max_length=4, choices=CONTRACTS, default=REGULAR_CONTRACT)
    outcome = models.ForeignKey(Outcome, null=True, blank=True)
    note = models.CharField(max_length=80, null=True, blank=True)
    assigned = models.CharField(max_length=20, null=True, blank=True) # this is something to do with the pod...

    def __unicode__(self):
        return u"%s - %s - %s" % (self.day.day, self.person, self.shift_type)

    def clean_fields(self, *args, **kwargs):
        if self.shift_type:
            for field in ['hours', 'start', 'end']:
                if getattr(self, field) is None:
                    setattr(self, field, getattr(self.shift_type, field))

    def clean(self, *args, **kwargs):
        super(Shift, self).clean(*args, **kwargs)
        if self.shift_type.mutex:
            other_shifts = (self.person.shifts.exclude(end__lte=self.start)
                .exclude(start__gte=self.end).prefetch_related('shift_type')
                .exclude(shift_type__mutex=False).values_list('id', flat=True))
            if other_shifts:
                raise ShiftsOverlapError(params={'shift_ids': other_shifts})


# class ShiftForm(ModelForm):
#     class Meta:
#         model = Shift
