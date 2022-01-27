from ssl import HAS_NEVER_CHECK_COMMON_NAME
from apps.models import Model

class Loan(Model):
    __table__ = 'records'
    __primary_key__ = 'no'