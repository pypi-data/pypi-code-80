from django.http import HttpResponse
from django.shortcuts import render

from .models import Event


def index(request):
    flashday = Event.objects.all()
    return HttpResponse(flashday)
