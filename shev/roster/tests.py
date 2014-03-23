from datetime import time, date

from django.forms import ValidationError
from django.test import TestCase

from shev.roster.models import TeamOrAgency, Person, ShiftType, Day
from shev.roster.exceptions import ShiftsOverlapError


class TestScheduling(TestCase):

    def setUp(self):
        self.team = TeamOrAgency.objects.create(label='A Team')
        self.bob = Person.objects.create(first_name='bob', last_name='smith',
            band=Person.BAND_7, team_or_agency=self.team)
        self.night_shift = ShiftType.objects.create(label='Clinical shift - N',
            hours=11.5, start=time(19, 45), end=time(8, 15), clinical=True,
            supernumeraryable=True, time_of_day=ShiftType.SHIFT_NIGHT)
        self.late_shift = ShiftType.objects.create(label='Clinical shift - Late',
            hours=7.5, start=time(12, 15), end=time(20, 15), clinical=True,
            supernumeraryable=True, time_of_day=ShiftType.SHIFT_LATE)
        self.annual_leave = ShiftType.objects.create(label='Annual Leave',
            hours=7.5, start=time(9, 0), end=time(17, 0), clinical=False, mutex=False)
        self.today = Day.objects.create(day=date(2014, 03, 24))
        self.tomorrow = Day.objects.create(day=date(2014, 03, 25))

    def test_reject_overlap(self):
        self.bob.shifts.create(day=self.today, shift_type=self.late_shift,
            end=time(16, 15))
        errored = False
        try:
            self.bob.shifts.create(day=self.today, shift_type=self.late_shift,
                start=time(16, 0))
        except ValidationError as e:
            errored = True
            all_codes = [error.code for error in e.error_dict['__all__']]
            self.assertIn(ShiftsOverlapError.code, all_codes)

        self.assertTrue(errored)

    def test_allow_annual_leave_overlap(self):
        self.bob.shifts.create(day=self.today, shift_type=self.late_shift,
            end=time(16, 15))
        self.bob.shifts.create(day=self.today, shift_type=self.annual_leave,
            start=time(16, 0))
