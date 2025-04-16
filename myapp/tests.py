from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import TourPackage

class TourPackageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.package = TourPackage.objects.create(
            name="Test Package",
            price=1000,
            duration=7111
        )

    def test_package_listing(self):
        self.assertEqual(f"{self.package.name}", "Test Package")
        self.assertEqual(self.package.price, 1000)

    def test_package_list_view(self):
        response = self.client.get(reverse('package_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Package")


class ReviewTests(TestCase):
    def test_add_review_view(self):
        response = self.client.get(reverse('add_review', args=[1]))
        self.assertEqual(response.status_code, 302)

class PackageDetailTests(TestCase):
    def setUp(self):
        self.package = TourPackage.objects.create(
            name="Test Package",
            price=1000,
            duration=7
        )

    def test_package_detail_view(self):
        response = self.client.get(reverse('package_detail', args=[self.package.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Package")