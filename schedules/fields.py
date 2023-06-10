import datetime
from django.utils.translation import gettext_lazy as _
from django.core import exceptions
from django.db.models.fields import DateTimeField as BaseDateTimeField
from schedules import forms as schedule_forms

class DateTimeField(BaseDateTimeField):
    default_error_messages = {
        'invalid': _('“%(value)s” value has an invalid format. It must be in '
                     'YYYY-MM-DD HH:MM format.'),
        'invalid_date': _("“%(value)s” value has the correct format "
                          "(YYYY-MM-DD) but it is an invalid date."),
        'invalid_datetime': _('“%(value)s” value has the correct format '
                              '(YYYY-MM-DD HH:MM) '
                              'but it is an invalid date/time.'),
    }
    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            return datetime.datetime(value.year, value.month, value.day, value.hour, value.minute, 0, 0, value.tzinfo)
        
        raise exceptions.ValidationError(
            self.error_messages['invalid'],
            code='invalid',
            params={'value': value},
        )
    def formfield(self, **kwargs):
        defaults = {"form_class": schedule_forms.DateTimeField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

