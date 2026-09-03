from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tracker.models import Category, Transaction


class DeleteTransactionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.category = Category.objects.create(name="Food")

        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=500.00,
            date=date.today(),
            category=self.category,
            description="Test transaction",
            transaction_type="EXPENSE",
        )

    def test_get_does_not_delete_transaction(self):
        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.get(
            reverse("delete_transaction", args=[self.transaction.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Transaction.objects.filter(pk=self.transaction.pk).exists()
        )

    def test_post_deletes_transaction(self):
        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.post(
            reverse("delete_transaction", args=[self.transaction.pk])
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertFalse(
            Transaction.objects.filter(pk=self.transaction.pk).exists()
        )