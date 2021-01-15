from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import django_filters
from django_filters import DateRangeFilter, DateFilter


class TransactionFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name='date',lookup_expr=('gt'),)
    end_date = DateFilter(field_name='date',lookup_expr=('lt'))
    date_range = DateRangeFilter(field_name='date')

    class Meta:
        model = Transaction
        fields =  [
        'type', 'contractor', 'category_expenses', 'category_income', 'send_to',
        'bank_account', 'specific_project',
        ]
