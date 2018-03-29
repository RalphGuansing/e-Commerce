from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class AlphaNumericPunctuationValidator:
	def __init__(self):
		pass

	def validate(self,password,user=None):
		m = re.search(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$',password)

		if m is None:
			raise ValidationError('Password should contain letters, numbers and punctuation!')

	def get_help_text(self):
		return _('Your password should contain alphanumeric and punctuation characters')