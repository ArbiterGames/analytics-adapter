from decimal import Decimal
from django.db import models


class Record(models.Model):
    date = models.DateField()
    revenue = models.CharField(max_length=100, default='0')
    dau = models.CharField(max_length=100, default='0', verbose_name='DAU')
    prize_pool_impact = models.CharField(max_length=100, default='0')

    @property
    def arpu(self):
        # Wrap in try in-case revenue or dau was 0
        try:
            return '{0:.2f}'.format(Decimal(self.revenue) / Decimal(self.dau))
        except:
            return '0'

    def __unicode__(self):
        return '%s' % self.date


class AlgorithmRecord(models.Model):
    date = models.DateField()
    version = models.CharField(max_length=10)
    value = models.CharField(max_length=10, default='0')
    record = models.ForeignKey(Record, null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.date
