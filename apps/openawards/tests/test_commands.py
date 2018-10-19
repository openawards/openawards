from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class GeneratefakedataTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('generateFakeData', stdout=out)
        self.assertNotIn('Failed to create data for model', out.getvalue())