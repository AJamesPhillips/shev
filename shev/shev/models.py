from django.db import models

BANDS = (("7","7"),
         ("6.5","6.5"),
         ("6","6"),
         ("5","5"),
         ("4","4"),
         ("2","2")
         )

class TeamOrAgency(models.Model):
    label = models.TextField()
    def __unicode__(self):
        return u"%s" % (self.label)

class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    band = models.CharField(max_length=5, choices=BANDS)
    team_or_agency = models.ForeignKey(TeamOrAgency)
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class ShiftType(models.Model):
    label = models.TextField()
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    def __unicode__(self):
        return u"%s:%s hours" % (self.label, self.hours)

class Outcome(models.Model):
    label = models.TextField()
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
    contract = models.CharField(max_length=4, choices=CNTRCTS)
    outcome = models.ForeignKey(Outcome)
    note = models.TextField(null=True, blank=True)
    assigned = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return u"%s - %s - %s" % (self.day.day, self.person, self.shift_type)
