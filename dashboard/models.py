from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PaymentSourceType(models.Model):
    handle = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.handle

    def __repr__(self):
        return 'PaymentSourceType(handle=\'%s\', description=\'%s\')' % (self.handle, self.description)


class PaymentSource(TimestampedModel):
    display_name = models.CharField(max_length=32, unique=True)
    source_type = models.ForeignKey(PaymentSourceType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='payment_source')

    def __str__(self):
        return '%s (%s)' % (self.display_name, self.source_type.handle)

    def __repr__(self):
        return 'PaymentSource(display_name=\'%s\', source_type=\'%s\', image=\'%s\')' % (
            self.display_name,
            self.source_type,
            self.image
        )


class Payee(TimestampedModel):
    name = models.CharField(max_length=64)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.name)

    def __repr__(self):
        return 'Payee(name=\'%s\', website=\'%s\')' % (self.name, self.website)


class ExpenseFrequency(models.Model):
    handle = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.handle

    def __repr__(self):
        return 'ExpenseFrequency(handle=\'%s\', description=\'%s\')' % (self.handle, self.description)


class Expense(TimestampedModel):
    description = models.CharField(max_length=140)
    amount = models.IntegerField(help_text='Value in subunits. 1 unit = 100 subunits.')
    currency = models.CharField(max_length=5)
    frequency = models.ForeignKey(ExpenseFrequency, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    payment_source = models.ForeignKey(PaymentSource, on_delete=models.CASCADE, related_name='expenses')
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE, related_name='expenses')
    billing_address = models.TextField()

    def __str__(self):
        return '%s%d for %s' % (self.currency, self.amount/100, self.description)

    def __repr__(self):
        return (
            'Expense(description=%s,\n'
            '\tamount=%d,\n'
            '\tcurrency=%s,\n'
            '\tfrequency=%s,\n'
            '\tstart_date=%s,\n'
            '\tend_date=%s,\n'
            '\tpayment_source=%s,\n'
            '\tpayee=%s,\n'
            '\tbilling_address=%s)'
            % (
                self.description,
                self.amount,
                self.currency,
                self.frequency,
                self.start_date,
                self.end_date,
                self.payment_source,
                self.payee,
                self.billing_address
            )
        )
