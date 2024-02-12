# myapp/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import UserProfile  
from .models import InventoryItem, Category, BuildDashboard

class MyAppViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = UserProfile.objects.create_user(username='testuser', email='testuser@example.com', password='Test1!@#')

        # Create test data for items, categories, and builds
        self.category = Category.objects.create(name='Raw Materials')
        self.item = InventoryItem.objects.create(
            sku='JNGLCOT',
            name='Cotton - Jungle Print',
            category=self.category,
            in_stock=18.75,
            available_stock=0
        )
        self.build = BuildDashboard.objects.create(
            references='Build 3-Pack Single Beeswax Wrap for SO #1004',
            item_group='3-packSingle Beeswax Wrap',
            quantity=10,
            cost=52.50,
            linked_sale_order_group='SO #1004',
            creation_group_date='2023-02-24',
            completion_group_date='2023-02-28'
        )

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'Test1!@#'})
        self.assertEqual(response.status_code, 302)  # Check if redirecting after successful login

    def test_user_register(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'Test1!@#', 'password2': 'Test1!@#'})
        self.assertEqual(response.status_code, 302)  # Check if redirecting after successful registration

    def test_user_logout(self):
        # Login before testing logout
        self.client.login(username='testuser', password='Test1!@#')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Check if redirecting after successful logout

    def test_add_item_view(self):
        response = self.client.post(reverse('add_item'), data={
            'sku': 'JNGLCOT',
            'name': 'Cotton - Jungle Print',
            'category': self.category.id,
            'in_stock': 18.75,
            'available_stock': 0
        })
        self.assertEqual(response.status_code, 302)  # Check if redirecting after successful item creation
        new_item = InventoryItem.objects.get(name='Cotton - Jungle Print')
        self.assertIsNotNone(new_item)

    def test_add_category_view(self):
        response = self.client.post(reverse('add_category'), data={'name': 'Raw Materials'})
        self.assertEqual(response.status_code, 302)  # Check if redirecting after successful category creation
        new_category = Category.objects.get(name='Raw Materials')
        self.assertIsNotNone(new_category)


    def test_add_build_view(self):
        response = self.client.post(reverse('add_build'), data={
            'references': 'Build 3-Pack Single Beeswax Wrap for SO #1004',
            'item_group': '3-packSingle Beeswax Wrap',
            'quantity': 10,
            'cost': 52.50,
            'linked_sale_order_group': 'SO #1004',
            'creation_group_date': '2023-02-24',
            'completion_group_date': '2023-02-28'
        })
        self.assertEqual(response.status_code, 302)  # Check if redirecting after successful build creation
        new_build = BuildDashboard.objects.get(references='Build 3-Pack Single Beeswax Wrap for SO #1004')
        self.assertIsNotNone(new_build)

    def test_home_api(self):
        response = self.client.get(reverse('home_api'))
        self.assertEqual(response.status_code, 200)
        json_data = "Cotton - Jungle Print"
        self.assertContains(response, json_data)

    def test_build_dashboard_api(self):
        response = self.client.get(reverse('build_dashboard_api'))
        self.assertEqual(response.status_code, 200)
        json_data = "Build 3-Pack Single Beeswax Wrap for SO #1004"
        self.assertContains(response, json_data)
