from django.test import TestCase

class TestViews(TestCase):

    def test_get_menu_page(self):
        response = self.client.get('/menu_page/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_page.html')