from django.db import models

BANDS = (("7","7"),
         ("6.5","6.5"),
         ("6","6"),
         ("5","5"),
         ("4","4"),
         ("2","2")
         )

class TeamOrAgency(models.Model):
    label = models.CharField(max_length=40)
    def __unicode__(self):
        return u"%s" % (self.label)
    class Meta:
        verbose_name_plural = "Teams and Agencies"

class Person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    band = models.CharField(max_length=5, choices=BANDS)
    team_or_agency = models.ForeignKey(TeamOrAgency)
## TODO
# Person needs a 'pod' and an ALEntitlement field?
#
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)
    class Meta:
        verbose_name_plural = "People"


class ShiftType(models.Model):
# todo major changes...
    label = models.CharField(max_length=40)
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    def __unicode__(self):
        return u"%s:%s hours" % (self.label, self.hours)

class Outcome(models.Model):
    label = models.CharField(max_length=100)
    def __unicode__(self):
        return u"%s" % (self.label)

CNTRCTS = (
    ("REGU","Regular"),
    ("BANK","Bank"),
    ("BNKL","Bank Line"),
    ("AGNC","Agency"),
    ("AGNL","Agency Line")
    )

class Day(models.Model):
    day = models.DateField()
    note = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return u"%s %s" % (self.day, self.note)

class Shift(models.Model):
    day = models.ForeignKey(Day)
    person = models.ForeignKey(Person)
    shift_type = models.ForeignKey(ShiftType)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
# TODO needs hours completed
    contract = models.CharField(max_length=4, choices=CNTRCTS)
    outcome = models.ForeignKey(Outcome)
    note = models.CharField(max_length=80,null=True, blank=True)
    assigned = models.CharField(max_length=20, null=True, blank=True) # this is something to do with the pod...
    
    def __unicode__(self):
        return u"%s - %s - %s" % (self.day.day, self.person, self.shift_type)
