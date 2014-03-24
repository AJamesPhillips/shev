from django.forms import ValidationError


class BaseValidationError(ValidationError):
    def __init__(self, params=None):
        # If suitable, provide a dict of relevant params
        kwargs = {'params': params} if params and isinstance(params, dict) else {}
        kwargs['code'] = self.code
        super(BaseValidationError, self).__init__(self.message, **kwargs)


class ShiftsOverlapError(BaseValidationError):
    code = 'SHIFT_OVERLAP'
    message = ('One or more shifts already scheduled ' +
        'for this person for this time period')


class DayNearNightError(BaseValidationError):
    code = 'DAY_NEAR_NIGHT'
    message = ('Person just came off, or about to start nights/days, so you can not schedule a day/night shift.')


class ShiftLacksTypeError(BaseValidationError):
    code = 'SHIFT_LACKS_TYPE'
    message = ('Please specify a type for this shift')


class ShiftLacksDayError(BaseValidationError):
    code = 'SHIFT_LACKS_DAY'
    message = ('Please specify a day for this shift')


class ShiftLacksTimeError(BaseValidationError):
    code = 'SHIFT_LACKS_TIME'
    message = ('Please specify a start and end for this shift')
