from django.urls import path
from .views import *


urlpatterns = [

    path('bank-account/', BankAccountList.as_view()),
    path('bank-account/<int:pk>/archivate/', BankAccountDetail.as_view()),
    path('bank-account/archive/', BankAccountArchiveList.as_view()),
    path('bank-account/archive/<int:pk>/restore/', BankAccountArchiveDetail.as_view()),
    path('bank-account/<int:pk>/hard-delete/', BankAccountHardDelete.as_view()),

    path('specific-project/', SpecificProjectList.as_view()),
    path('specific-project/<int:pk>/archivate/', SpecificProjectDetail.as_view()),
    path('specific-project/archive/', SpecificProjectArchiveList.as_view()),
    path('specific-project/archive/<int:pk>/restore/', SpecificProjectArchiveDetail.as_view()),
    path('specific-project/<int:pk>/hard-delete/', SpecificProjectHardDelete.as_view()),

    path('contractor/', ContractorList.as_view()),
    path('contractor/<int:pk>/', ContractorDetail.as_view()),

    path('category-income/', CategoryIncomeList.as_view()),
    path('category-income/<int:pk>/', CategoryIncomeDetail.as_view()),

    path('category-expenses/', CategoryExpensesList.as_view()),
    path('category-expenses/<int:pk>/', CategoryExpensesDetail.as_view()),

    path('transaction/', TransactionList.as_view()),
    path('transaction/<int:pk>/', TransactionDetail.as_view()),

    path('total/', TotalList.as_view()),
    path('total/<int:pk>/', TotalDetail.as_view()),

]
