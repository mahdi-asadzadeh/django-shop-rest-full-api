from rest_framework.test import APITestCase
from django.urls import reverse


class TestCategoryMainView(APITestCase):
    def test_category_main_GET(self):
        response = self.client.get(reverse('category:category_main'))
        self.assertEqual(200, response.status_code)
