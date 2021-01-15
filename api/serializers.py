from rest_framework import serializers
from .models import *


class BankAccountSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField()

    class Meta:
        model = BankAccount
        fields = ['id', 'name_bank', 'balance']


class ContractorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contractor
        fields = ['id', 'name', 'email']


class CategoryIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryIncome
        fields = ['id', 'name']


class CategoryExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryExpenses
        fields = ['id', 'name']


class SpecificProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecificProject
        fields = ['id', 'name']


class TransactionSerializer(serializers.ModelSerializer):

    date = serializers.DateField()
    bank_account = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all())
    contractor = serializers.PrimaryKeyRelatedField(
        queryset=Contractor.objects.all(), allow_null=True)
    category_income = serializers.PrimaryKeyRelatedField(
        queryset=CategoryIncome.objects.all(), allow_null=True)
    category_expenses = serializers.PrimaryKeyRelatedField(
        queryset=CategoryExpenses.objects.all(), allow_null=True)
    specific_project = serializers.PrimaryKeyRelatedField(
        queryset=SpecificProject.objects.all(), allow_null=True)
    send_to = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all(), allow_null=True)



    class Meta:
        model = Transaction
        fields = [
            'id', 'date', 'sum', 'type', 'description', 'bank_account',
            'category_income', 'category_expenses', 'contractor',
            'specific_project', 'send_to',
        ]
        depth = 1

    def to_representation(self, value):

        data = super().to_representation(value)
        banks = BankAccountSerializer(value.bank_account)
        contractors = ContractorSerializer(value.contractor)
        category_in = CategoryIncomeSerializer(value.category_income)
        category_ex = CategoryExpensesSerializer(value.category_expenses)
        specific_projects = SpecificProjectSerializer(value.specific_project)
        bank_to = BankAccountSerializer(value.send_to)

        data['send_to'] = bank_to.data
        data['category_expenses'] = category_ex.data
        data['bank_account'] = banks.data
        data['contractor'] = contractors.data
        data['category_income'] = category_in.data
        data['specific_project']  = specific_projects.data

        return data


class TotalSerializer(serializers.ModelSerializer):

    total_expenses = serializers.FloatField(
        source='get_total_expenses', read_only=True)
    total_income = serializers.FloatField(
        source='get_total_income', read_only=True)
    profit = serializers.FloatField(
        source='get_profit', read_only=True)

    class Meta:
        model = Total
        fields = ['id', 'total_income', 'total_expenses', 'profit']

