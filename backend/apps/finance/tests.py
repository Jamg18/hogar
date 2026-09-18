from decimal import Decimal

from rest_framework.test import APITestCase

from apps.finance.models import Category, Transaction
from apps.users.models import User


class FinanceApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("casa@example.com", "clave-segura", name="Casa")
        self.client.force_authenticate(self.user)
        self.category = Category.objects.get(household__memberships__user=self.user, name="Alimentación")

    def test_registering_expense_updates_monthly_summary(self):
        response = self.client.post("/api/v1/transactions/", {
            "type": "expense", "amount": "48.35", "currency": "EUR",
            "category": str(self.category.id), "effective_date": "2026-09-18", "note": "Compra semanal",
        }, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)

        response = self.client.get("/api/v1/finance/summary/?month=2026-09")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(response.data["expense"]), Decimal("48.35"))
        self.assertEqual(Decimal(response.data["balance"]), Decimal("-48.35"))

    def test_category_must_match_transaction_type(self):
        response = self.client.post("/api/v1/transactions/", {
            "type": "income", "amount": "48.35", "category": str(self.category.id), "effective_date": "2026-09-18",
        }, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("category", response.data)
