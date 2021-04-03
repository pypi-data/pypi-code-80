from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Event


class Home(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)
