from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from unidecode import unidecode


@deconstructible
class AlphanumericExcludingDiacritic:
    """
    Alle alfanumerieke tekens m.u.v. diacrieten.
    """

    def __init__(self, start=0):
        self.start = start

    def __call__(self, value):
        stripped_value = value[self.start:]
        non_diactric = unidecode(stripped_value)
        non_diactric.encode('ascii')
        if stripped_value != non_diactric:
            raise ValidationError(
                'Waarde "{0}" mag geen diakrieten of non-ascii tekens bevatten{1}'.format(
                    value, ' na de eerste {0} karakters'.format(self.start) if self.start else ''
                )
            )

    def __eq__(self, other):
        return isinstance(other, AlphanumericExcludingDiacritic) and self.start == other.start


# Default validator for entire string.
alphanumeric_excluding_diacritic = AlphanumericExcludingDiacritic()
