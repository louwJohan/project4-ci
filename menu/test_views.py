from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client
from .models import FoodMenu


class TestViews(TestCase):
    """
    Tests of all the views of Menu app.
    Tests display , edit ,create and delete methods
    """
    def setUp(self):
        """
        Setup users with different status
        """
        self.client = Client()
        self.user = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword')
        self.user = User.objects.create_superuser('admin',
                                                  'admin@mail.com',
                                                  'adminpassword')

    def test_get_menu_page(self):
        """
        Function tests get menu page
        """
        response = self.client.get(reverse('menu_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_page.html')

    def test_get_menu_list_page_authorized(self):
        """
        Function tests get menu list page if user is_staff
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_list.html')

    def test_get_menu_list_page_unauthorized(self):
        """
        Function tests get menu list page if user not is_staff
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 403)

    def test_get_menu_delete_item_page(self):
        """
        Function tests get menu delete page if user is_staff
        """
        self.client.login(username='admin', password='adminpassword')
        item = FoodMenu.objects.create(title='Test Item',
                                       description='New Item',
                                       course=0,
                                       price=5)
        response = self.client.get(f'/menu_page/item_delete/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/item_delete.html')

    def test_get_item_create_form_page_unauthorizes_user(self):
        """
        Function tests get item create form page if user not is_staff
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('item_create_form'))
        self.assertEqual(response.status_code, 403)

    def test_get_item_create_form_page_authorizes_user(self):
        """
        Function tests get item create form page if user is_staff
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('item_create_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/item_create_form.html')

    def test_get_menu_edit_item_page(self):
        """
        Function tests get menu edit item page if user is_staff
        """
        self.client.login(username='admin', password='adminpassword')
        item = FoodMenu.objects.create(title='Test Item',
                                       description='New Item',
                                       course=0,
                                       price=5)
        response = self.client.get(f'/menu_page/item_update_form/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/item_update_form.html')

    def test_delete_menu_item(self):
        """Function to check whether a menu item can be deleted."""
        self.client.login(username='admin', password='adminpassword')
        item = FoodMenu.objects.create(title='Test Item',
                                       description='New Item',
                                       course=0,
                                       price=5)
        existing_items = FoodMenu.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 1)
        response = self.client.post(f'/menu_page/item_delete/{item.id}')
        self.assertRedirects(response, reverse('menu_list'))
        existing_items = FoodMenu.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    def test_edit_menu_item(self):
        """Function to check whether a menu item can be updated."""
        self.client.login(username='admin', password='adminpassword')
        item = FoodMenu.objects.create(title='Test Item',
                                       description='New Item',
                                       course=0,
                                       price=5)
        response = self.client.post(f'/menu_page/item_update_form/{item.id}',
                                    {
                                        'title': 'Test Edit Item check',
                                        'description': 'New Item',
                                        'course': 0,
                                        'price': 5,
                                    })
        self.assertEqual(response.status_code, 302)
        updated_item = FoodMenu.objects.get(id=item.id)
        self.assertEqual(updated_item.title, 'Test Edit Item check')

    def test_get_menu_item_detail_page(self):
        """
        Function tests get menu item page
        """
        self.client.login(username='admin', password='adminpassword')
        item = FoodMenu.objects.create(title='Test Item',
                                       description='New Item',
                                       course=0,
                                       price=5)
        response = self.client.get(f'/menu_page/item_detail/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/item_detail.html')

    def test_create_new_menu_item(self):
        """
        Function tests if you can create new menu item
        """
        self.client.login(username='admin', password='adminpassword')
        items = FoodMenu.objects.all()
        self.assertEqual(len(items), 0)
        response = self.client.post('/menu_page/item_create_form',
                                    {
                                        'title': 'Test New Item check',
                                        'description': 'New Item',
                                        'course': 0,
                                        'price': 5,
                                    })
        self.assertEqual(response.status_code, 302)
        new_items = FoodMenu.objects.all()
        self.assertEqual(len(new_items), 1)
