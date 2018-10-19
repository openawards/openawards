from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class GenerateFakeDataTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('generateFakeData', stdout=out, test=True, works=5, users=5)
        self.assertNotIn('Failed to create data for model', out.getvalue())
