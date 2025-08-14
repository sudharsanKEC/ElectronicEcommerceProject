from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def rolePage(request):
    return render(request,"RoleSelection.html")