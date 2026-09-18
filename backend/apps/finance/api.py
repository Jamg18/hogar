from datetime import date

from django.db.models import Q, Sum
from django.utils.dateparse import parse_date
from rest_framework import serializers, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.households.models import Household

from .models import Category, Transaction, TransactionType


def current_household(request):
    household_id = request.query_params.get("household_id")
    memberships = request.user.memberships.select_related("household")
    if household_id:
        membership = memberships.filter(household_id=household_id).first()
    else:
        membership = memberships.order_by("created_at").first()
    if not membership:
        raise PermissionDenied("No tienes acceso a ningún hogar.")
    return membership.household


class CategorySerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(source="transaction_type", choices=TransactionType.choices)

    class Meta:
        model = Category
        fields = ["id", "name", "type", "color", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(source="transaction_type", choices=TransactionType.choices)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "type", "amount", "currency", "category", "category_name", "effective_date", "note", "source", "created_at", "updated_at"]
        read_only_fields = ["id", "source", "created_at", "updated_at"]

    def validate(self, attrs):
        household = self.context["household"]
        category = attrs.get("category", getattr(self.instance, "category", None))
        transaction_type = attrs.get("transaction_type", getattr(self.instance, "transaction_type", None))
        if category and category.household_id != household.id:
            raise ValidationError({"category": "La categoría no pertenece al hogar actual."})
        if category and category.transaction_type != transaction_type:
            raise ValidationError({"category": "La categoría debe ser del mismo tipo que el movimiento."})
        return attrs

    def create(self, validated_data):
        return Transaction.objects.create(household=self.context["household"], **validated_data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_household(self):
        return current_household(self.request)

    def get_queryset(self):
        household = self.get_household()
        queryset = Category.objects.filter(household=household)
        category_type = self.request.query_params.get("type")
        if category_type:
            queryset = queryset.filter(transaction_type=category_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(household=self.get_household())


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_household(self):
        return current_household(self.request)

    def get_queryset(self):
        queryset = Transaction.objects.filter(household=self.get_household(), deleted_at__isnull=True).select_related("category")
        for key, lookup in (("from", "effective_date__gte"), ("to", "effective_date__lte"), ("type", "transaction_type"), ("category", "category_id")):
            if value := self.request.query_params.get(key):
                queryset = queryset.filter(**{lookup: value})
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["household"] = self.get_household()
        return context

    def perform_destroy(self, instance):
        if instance.source == Transaction.Source.MANUAL:
            instance.delete()
        else:
            instance.archive()


class MonthlySummaryView(APIView):
    def get(self, request):
        try:
            year, month = (int(value) for value in request.query_params.get("month", "").split("-"))
            start = date(year, month, 1)
        except (TypeError, ValueError):
            raise ValidationError({"month": "Usa el formato AAAA-MM."})
        end = date(year + (month == 12), 1 if month == 12 else month + 1, 1)
        totals = Transaction.objects.filter(household=current_household(request), deleted_at__isnull=True, effective_date__gte=start, effective_date__lt=end).values("transaction_type").annotate(total=Sum("amount"))
        values = {item["transaction_type"]: item["total"] for item in totals}
        income = values.get(TransactionType.INCOME, 0)
        expense = values.get(TransactionType.EXPENSE, 0)
        return Response({"month": request.query_params["month"], "income": income, "expense": expense, "balance": income - expense})
