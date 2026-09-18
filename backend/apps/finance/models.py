import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.households.models import Household


class TransactionType(models.TextChoices):
    INCOME = "income", "Ingreso"
    EXPENSE = "expense", "Gasto"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey(Household, null=True, blank=True, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=80)
    transaction_type = models.CharField(max_length=7, choices=TransactionType.choices)
    color = models.CharField(max_length=7, default="#607D8B")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["transaction_type", "name"]
        constraints = [models.UniqueConstraint(fields=["household", "name", "transaction_type"], name="unique_category_per_household")]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    class Source(models.TextChoices):
        MANUAL = "manual", "Manual"
        SHOPPING = "shopping", "Compras"
        FUEL = "fuel", "Combustible"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    household = models.ForeignKey(Household, on_delete=models.PROTECT, related_name="transactions")
    transaction_type = models.CharField(max_length=7, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    currency = models.CharField(max_length=3, default="EUR")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    effective_date = models.DateField()
    note = models.CharField(max_length=500, blank=True)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.MANUAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-effective_date", "-created_at"]
        indexes = [models.Index(fields=["household", "effective_date"])]

    def clean(self):
        if self.category_id and self.category.transaction_type != self.transaction_type:
            from django.core.exceptions import ValidationError
            raise ValidationError({"category": "La categoría debe ser del mismo tipo que el movimiento."})

    def archive(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])
