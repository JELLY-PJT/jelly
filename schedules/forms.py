import datetime
from django.forms import DateTimeField as BaseDateTimeField

class DateTimeField(BaseDateTimeField):
    input_formats = [
        "%Y-%m-%d %H:%M",  # '2006-10-25 14:30:59'
    ]
    output_formats = [
        "%Y-%m-%d %H:%M",  # '2006-10-25 14:30:59'
    ]
    def to_python(self, value):
        """
        Validate that the input can be converted to a datetime. Return a
        Python datetime.datetime object.
        """
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return datetime.datetime(value.year, value.month, value.day, value.hour, value.minute, 0, 0, value.tzinfo)

