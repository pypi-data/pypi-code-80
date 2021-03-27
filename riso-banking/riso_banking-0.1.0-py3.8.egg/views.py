# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Config,
	BankAccount,
	CardAccount,
	Wallet,
	Transaction,
)


class ConfigCreateView(CreateView):

    model = Config


class ConfigDeleteView(DeleteView):

    model = Config


class ConfigDetailView(DetailView):

    model = Config


class ConfigUpdateView(UpdateView):

    model = Config


class ConfigListView(ListView):

    model = Config


class BankAccountCreateView(CreateView):

    model = BankAccount


class BankAccountDeleteView(DeleteView):

    model = BankAccount


class BankAccountDetailView(DetailView):

    model = BankAccount


class BankAccountUpdateView(UpdateView):

    model = BankAccount


class BankAccountListView(ListView):

    model = BankAccount


class CardAccountCreateView(CreateView):

    model = CardAccount


class CardAccountDeleteView(DeleteView):

    model = CardAccount


class CardAccountDetailView(DetailView):

    model = CardAccount


class CardAccountUpdateView(UpdateView):

    model = CardAccount


class CardAccountListView(ListView):

    model = CardAccount


class WalletCreateView(CreateView):

    model = Wallet


class WalletDeleteView(DeleteView):

    model = Wallet


class WalletDetailView(DetailView):

    model = Wallet


class WalletUpdateView(UpdateView):

    model = Wallet


class WalletListView(ListView):

    model = Wallet


class TransactionCreateView(CreateView):

    model = Transaction


class TransactionDeleteView(DeleteView):

    model = Transaction


class TransactionDetailView(DetailView):

    model = Transaction


class TransactionUpdateView(UpdateView):

    model = Transaction


class TransactionListView(ListView):

    model = Transaction

