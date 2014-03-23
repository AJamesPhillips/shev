from django.db import models


BANDS = (("7","7"),
         ("6.5","6.5"),
         ("6","6"),
         ("5","5"),
         ("4","4"),
         ("2","2"),
         )


class TeamOrAgency(models.Model):
    class Meta:
        verbose_name_plural = "Teams and Agencies"

    label = models.CharField(max_length=40)

    def __unicode__(self):
        return u"%s" % (self.label)


class Person(models.Model):
    class Meta:
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


class ShiftType(models.Model):
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
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    clinical = models.BooleanField()
    supernumeraryable = models.BooleanField(default=False)  # sorry for the name
    time_of_day = models.CharField(null=True, max_length=10, choices=SHIFT_CHOICES)

    def __unicode__(self):
        return u"%s:%s hours" % (self.label, self.hours)


class Outcome(models.Model):
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


class Day(models.Model):
    day = models.DateField()
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.day, self.note)


class Shift(models.Model):
    REGULAR_CONTRACT = "REGU"
    CONTRACTS = (
        (REGULAR_CONTRACT, "Regular"),
        ("BNKL", "Bank Line"),
        ("BANK", "Bank"),
        ("AGNL", "Agency Line"),
        ("AGNC", "Agency"),
    )

    day = models.ForeignKey(Day)
    person = models.ForeignKey(Person)
    shift_type = models.ForeignKey(ShiftType)
    supernumerary = models.BooleanField(default=False)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    contract = models.CharField(max_length=4, choices=CONTRACTS, default=REGULAR_CONTRACT)
    outcome = models.ForeignKey(Outcome)
    note = models.CharField(max_length=80,null=True, blank=True)
    assigned = models.CharField(max_length=20, null=True, blank=True) # this is something to do with the pod...

    def __unicode__(self):
        return u"%s - %s - %s" % (self.day.day, self.person, self.shift_type)
