from django.test import TestCase

from app.functions import addition


class FunctionTests(TestCase):

    def test_function(self):
        self.assertEqual(addition(2,3), 5)