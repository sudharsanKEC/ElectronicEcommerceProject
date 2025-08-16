from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import *
# Create your views here.

def rolePage(request):
    return render(request,"RoleSelection.html")

def webAppAdminLogin(request):
    return render(request,"WebAdminLoginPage.html")

def webAdminValidation(request):
    if request.method=="POST":
        email = request.POST['email']        
        location = request.POST['location']
        password = request.POST['password']

        waa = WebAppAdmin.objects.filter(email=email,district=location).first()
        if waa:
            if(waa.password == password):
                return redirect("waaDashboard",id = waa.unique_id) # the name id and the <str:id> should match exactky
            else:
                messages.error(request,"Invalid credentials")
                return redirect("waaLogin")
        else:
            messages.error("Account doesn't exist")
            return redirect("waaLogin")
def webAppAdminDashboard(request,id):
    waa = WebAppAdmin.objects.filter(unique_id = id).first()
    return render(request,"WaaDashboard.html",
                {
                    "appAdmin":waa,
                }  
                )
        