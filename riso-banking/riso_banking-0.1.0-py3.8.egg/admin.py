# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import (
   Config,
   BankAccount,
   CardAccount,
   Wallet,
   Transaction,
)


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(CardAccount)
class CardAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass



