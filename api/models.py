from django.db import models
from django.db.models import Sum, F #for calculate data in models

from softdelete.models import SoftDeleteModel #archivate abctract model


class BankAccount(SoftDeleteModel):
    """
    Model for bank account
    """
    name_bank = models.CharField(max_length=100)
    balance = models.IntegerField()

    def __str__(self):
        return self.name_bank


class Contractor(models.Model):
    """
    The contractor is the person who made this transaction
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CategoryIncome(models.Model):
    """
    Model of categories for which money increases
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CategoryExpenses(models.Model):
    """
    Model for categories of expenses on which money is spent
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SpecificProject(SoftDeleteModel):
    """
    A model to know for which particular project or course
    the transaction is being made
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Model for transactions
    """

    INCOME = 'Income'
    EXPENSES = 'Expenses'
    BANK_TRANSACTION = 'BankTransaction'

    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSES, 'Expenses'),
        (BANK_TRANSACTION, 'BankTransaction'),
    ]


    date = models.DateField(auto_now_add=False)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    sum = models.IntegerField()
    bank_account = models.ForeignKey(
        'BankAccount', null=True, blank=True, on_delete=models.SET_NULL
        )
    category_expenses = models.ForeignKey(
        'CategoryExpenses', blank=True, null=True, on_delete=models.SET_NULL
        )
    category_income = models.ForeignKey(
        'CategoryIncome', blank=True, null=True, on_delete=models.SET_NULL
        )
    contractor = models.ForeignKey(
        'Contractor', null=True, blank=True, on_delete=models.SET_NULL
        )
    specific_project = models.ForeignKey(
        'SpecificProject', null=True, blank=True, on_delete=models.SET_NULL
        )
    send_to = models.ForeignKey(
        'BankAccount', on_delete=models.SET_NULL, blank=True,
        null=True, related_name='send_to'
        )

    description = models.TextField(max_length=100, null=True, blank=True)



    def save(self, *args, **kwargs):
        """ This function transfers money between accounts """
        if self.type == 'Income':
            BankAccount.objects.filter(
            id=self.bank_account.id).update(balance=F('balance') + self.sum
            )

        if self.type == 'Expenses':
            BankAccount.objects.filter(
            id=self.bank_account.id).update(balance=F('balance') - self.sum
            )

        if self.type == 'BankTransaction':
            BankAccount.objects.filter(
                id=self.bank_account.id).update(balance=F('balance') - self.sum)
            BankAccount.objects.filter(
                id=self.send_to.id).update(balance=F('balance') + self.sum)

        return super(Transaction, self).save(*args, **kwargs)


    def __str__(self):
        return self.type


class Total(models.Model):
    """
    Model for calculate the amount of income and expenses
    """
    date = models.DateTimeField(null=True, blank=True)

    def get_total_income(self):
        """
        Calculate total sum expenses
        """
        total = Transaction.objects.filter(type='Income').aggregate(total_income=Sum('sum'))
        return total.get('total_income')

    def get_total_expenses(self):
        """
        Calculate total sum expenses
        """
        total = Transaction.objects.filter(type='Expenses').aggregate(total_expenses=Sum('sum'))
        return total.get('total_expenses')

    def get_profit(self):
        """
        Calculate profit company
        """
        if self.get_total_expenses == None:
            self.get_total_expenses = 0
        else:
            profit = self.get_total_income() - self.get_total_expenses()
            return profit

    def save(self, *args, **kwargs):
        return super(Total, self).save(*args, **kwargs)
