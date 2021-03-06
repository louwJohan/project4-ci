from django.test import TestCase


class TestViews(TestCase):

    def test_get_home_page(self):
        """
        Function tests get home page
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
