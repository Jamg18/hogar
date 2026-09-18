from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.finance.models import Category, TransactionType
from apps.users.models import User

from .models import Household, Membership

DEFAULT_CATEGORIES = {
    TransactionType.EXPENSE: ["Alimentación", "Vivienda", "Suministros", "Transporte", "Combustible", "Salud", "Ocio", "Suscripciones", "Educación", "Mascotas", "Otros"],
    TransactionType.INCOME: ["Salario", "Extra", "Reembolso", "Venta", "Otros"],
}


@receiver(post_save, sender=User)
def create_initial_household(sender, instance, created, **kwargs):
    if not created:
        return
    household = Household.objects.create(name=f"Hogar de {instance.name or instance.email}")
    Membership.objects.create(household=household, user=instance, role=Membership.Role.OWNER)
    Category.objects.bulk_create([
        Category(household=household, name=name, transaction_type=transaction_type)
        for transaction_type, names in DEFAULT_CATEGORIES.items()
        for name in names
    ])
