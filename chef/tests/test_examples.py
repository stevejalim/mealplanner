from django.test import TestCase


class ExampleTests(TestCase):
    def test_addition(self):
        result = 27 + 95

        self.assertEqual(result, 122)

    def test_subtraction(self):

        result = 27 - 95

        self.assertEqual(result, -68)
