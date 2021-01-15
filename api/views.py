from .models import *
from .serializers import *
from api.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from drf_renderer_xlsx.mixins import XLSXFileMixin #export to xlsx
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination #pagination
from rest_framework.permissions import AllowAny
from rest_framework import status

class BankAccountList(generics.ListCreateAPIView):
    queryset = BankAccount.objects.get_queryset()
    serializer_class = BankAccountSerializer


class BankAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.balance > 0:
            content = [{
        "error":"Для сохранениня целостности ваших данных: Удалить счёт можно будет только с нулевым балансом"
            }]
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


class BankAccountArchiveList(generics.ListAPIView):
    queryset = BankAccount.objects.get_deleted()
    serializer_class = BankAccountSerializer

class BankAccountArchiveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.get_deleted()
    serializer_class = BankAccountSerializer

    def perform_destroy(self, instance):
        instance.undelete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BankAccountHardDelete(generics.RetrieveDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def perform_destroy(self, instance):
        instance.hard_delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecificProjectList(generics.ListCreateAPIView):
    queryset = SpecificProject.objects.all()
    serializer_class = SpecificProjectSerializer


class SpecificProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpecificProject.objects.all()
    serializer_class = SpecificProjectSerializer


class SpecificProjectArchiveList(generics.ListAPIView):
    queryset = SpecificProject.objects.get_deleted()
    serializer_class = SpecificProjectSerializer


class SpecificProjectArchiveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpecificProject.objects.get_deleted()
    serializer_class = SpecificProjectSerializer

    def perform_destroy(self, instance):
        instance.undelete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SpecificProjectHardDelete(generics.RetrieveDestroyAPIView):
    queryset = SpecificProject.objects.all()
    serializer_class = SpecificProjectSerializer

    def perform_destroy(self, instance):
        instance.hard_delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class TransactionList(XLSXFileMixin, generics.ListCreateAPIView):
    queryset = Transaction.objects.order_by('-date')
    serializer_class = TransactionSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TransactionFilter
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]
    filename = 'transaction.xlsx'

    column_header = {
        'titles': [
            "Id",
            "Date",
            "Sum",
            "Type",
            "Description",
            "BankId",
            "BankName",
            "BankBalance",
            "CategoryIncomeId",
            "CategoryIncome",
            "CategoryExpenseId",
            "CategoryExpense",
            "ContractorId",
            "Contractor",
            "ContractorEmail",
            "ProjectId",
            "Project",
            "SendToBankId",
            "SendToBank",
            "SendToBankBalance"
        ],
        'height': 20,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 10,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }
    body = {
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 12,
                'bold': False,
                'color': 'FF000000',
            }
        },
        'height': 20,
    }



class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class ContractorList(generics.ListCreateAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer


class ContractorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer


class CategoryIncomeList(generics.ListCreateAPIView):
    queryset = CategoryIncome.objects.all()
    serializer_class = CategoryIncomeSerializer


class CategoryIncomeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryIncome.objects.all()
    serializer_class = CategoryIncomeSerializer


class CategoryExpensesList(generics.ListCreateAPIView):
    queryset = CategoryExpenses.objects.all()
    serializer_class = CategoryExpensesSerializer


class CategoryExpensesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryExpenses.objects.all()
    serializer_class = CategoryExpensesSerializer


class TotalList(generics.ListCreateAPIView):
    queryset = Total.objects.all()
    serializer_class = TotalSerializer


class TotalDetail(generics.RetrieveUpdateDestroyAPIView):
     queryset = Total.objects.all()
     serializer_class = TotalSerializer
