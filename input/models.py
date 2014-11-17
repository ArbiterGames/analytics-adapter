from decimal import Decimal
from django.db import models


class Record(models.Model):
    date = models.DateField()
    revenue = models.CharField(max_length=100)
    dau = models.CharField(max_length=100)

    @property
    def arpu(self):
        # Wrap in try in-case revenue or dau was 0
        try:
            return '{0:.2f}'.format(Decimal(self.revenue) / Decimal(self.dau))
        except:
            return '0'

    def __unicode__(self):
        return '%s' % self.date
