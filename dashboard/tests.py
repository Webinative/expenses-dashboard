from django.test import TestCase
from django.utils import timezone
from .models import *
from .utils import *

# Create your tests here.


class TestGetMonthlyExpenses(TestCase):
    """test cases for utils.get_monthly_expenses
    """

    def setUp(self):
        bank_account = PaymentSourceType.objects.get(handle='BANK_ACCOUNT')
        monthly = ExpenseFrequency.objects.get(handle='MONTHLY')
        yearly = ExpenseFrequency.objects.get(handle='YEARLY')

        payee = Payee(name='MyPayee')
        payee.save()

        barclays = PaymentSource(display_name='Barclays', source_type=bank_account)
        barclays.save()

        now = timezone.now()

        # MONTHLY: From 1st Dec last year till 31st May this year
        expense = Expense(
            description='Exp_1',
            amount=100,
            currency='£',
            frequency=monthly,
            start_date=timezone.datetime(now.year - 1, 12, 1),
            end_date=timezone.datetime(now.year, 5, 31),
            payment_source=barclays,
            payee=payee,
            billing_address=(
                'Apple Inc\n',
                '1 Infinite loop\n'
                'San Francisco'
            )
        )
        expense.save()

        # MONTHLY: From 1st July till 30th Nov this year
        expense_2 = Expense(
            description='Exp_1.1',
            amount=101,
            currency='$',
            frequency=monthly,
            start_date=timezone.datetime(now.year, 7, 1),
            end_date=timezone.datetime(now.year, 11, 30),
            payment_source=barclays,
            payee=payee,
            billing_address=(
                'Microsoft Corporation\n',
                'Redmond'
            )
        )
        expense_2.save()

        # MONTHLY: From 15th Sep till 15th Dec this year
        expense_3 = Expense(
            description='Exp_1.2',
            amount=102,
            currency='£',
            frequency=monthly,
            start_date=timezone.datetime(now.year, 9, 15),
            end_date=timezone.datetime(now.year, 12, 15),
            payment_source=barclays,
            payee=payee,
            billing_address=(
                'Zoho Corporation\n',
                'Chennai'
            )
        )
        expense_3.save()

        self.now = now

    def test_get_yearly_expenses(self):
        pass

    def test_get_monthly_expenses_for_case_1(self):
        """Monthly expense that started last year and ends next month should be returned
        """
        expenses = get_monthly_expenses(self.now.year, 5)
        self.assertEqual(len(expenses), 1)

    def test_get_monthly_expenses_for_case_2(self):
        """Monthly expense that ended last month should NOT be returned
        """
        expenses = get_monthly_expenses(self.now.year, 6)
        self.assertEqual(len(expenses), 0)

    def test_get_monthly_expenses_for_case_3(self):
        """Monthly expense that starts in the current month should be returned
        """
        expenses = get_monthly_expenses(self.now.year, 7)
        self.assertEqual(len(expenses), 1)

        first: Expense = expenses.first()
        self.assertEqual('Exp_1.1', first.description)
        self.assertEqual('$', first.currency)

    def test_get_monthly_expense_for_case_4(self):
        """Monthly expense that starts mid-month should be returned
        """
        expenses = get_monthly_expenses(self.now.year, 9)
        self.assertEqual(len(expenses), 2)

        first: Expense = expenses.first()
        self.assertEqual('Exp_1.1', first.description)
        self.assertEqual('$', first.currency)

        second: Expense = expenses.last()
        self.assertEqual('Exp_1.2', second.description)
        self.assertEqual('£', second.currency)

    def test_get_monthly_expense_for_case_5(self):
        """Monthly expense that starts next month should NOT be returned
        """
        expenses = get_monthly_expenses(self.now.year, 6)
        self.assertEqual(len(expenses), 0)
