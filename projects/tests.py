from django.test import TestCase
from django.urls import reverse
from .models import BB

class AppTests(TestCase):
    
    def test_bbs_home_page(self):
        response = self.client.get(reverse('bbs_home'))
        self.assertEqual(response.status_code, 200)
        
    def test_molecules_home_page(self):
        response = self.client.get(reverse('molecules_home'))
        self.assertEqual(response.status_code, 200)
