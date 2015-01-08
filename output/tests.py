import json
from decimal import Decimal

from django.test import TestCase
from django.core.management import call_command
from django.test.client import Client
from django.core.urlresolvers import reverse

from input.models import Record
from input.models import AlgorithmRecord
from adapter.utils import Logger
logger = Logger()


class Functional(TestCase):
    made_call_to_get_data = False

    def setUp(self):
        if self.made_call_to_get_data == False:
            call_command('getmixpaneldata')
            self.made_call_to_get_data = True

    def test_alg_value_factors_in_dau(self):
        record = Record.objects.first()
        alg_rec_with_value = None
        for alg_record in AlgorithmRecord.objects.all():
            if float(alg_record.value) > 0:
                alg_rec_with_value = alg_record
                break
        total_value = alg_rec_with_value.value
        dau = record.dau
        c = Client()
        r = c.get(reverse('geckoboard_algorithm_arpu'))
        all_alg_data = json.loads(r.content)['series']
        current_alg_data = [d['data'] for d in all_alg_data if d['name'] == alg_rec_with_value.version]
        latest_value = current_alg_data[0][-1]
        expected_value = float('{0:.2f}'.format(Decimal(total_value) / Decimal(dau)))
        self.assertEqual(latest_value, expected_value)
