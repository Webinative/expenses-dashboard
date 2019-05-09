from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(User, UserAdmin)


class PaymentSourceTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: PaymentSourceType):
        return '%s' % obj.description


class PaymentSourceAdminForm(forms.ModelForm):
    source_type = PaymentSourceTypeChoiceField(queryset=PaymentSourceType.objects.all())

    class Meta:
        model = PaymentSource
        fields = '__all__'


@admin.register(PaymentSource)
class PaymentSourceAdmin(admin.ModelAdmin):
    form = PaymentSourceAdminForm


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    pass


class ExpenseFrequenceChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: ExpenseFrequency):
        return '%s' % obj.description


class ExpenseAdminForm(forms.ModelForm):
    frequency = ExpenseFrequenceChoiceField(queryset=ExpenseFrequency.objects.all())

    class Meta:
        model = Expense
        fields = '__all__'


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseAdminForm
