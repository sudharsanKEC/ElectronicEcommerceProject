from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import *
# Create your views here.

def rolePage(request):
    return render(request,"RoleSelection.html")

def webAppAdminLogin(request):
    return render(request,"WebAppAdmin/WebAdminLoginPage.html")

def webAdminValidation(request):
    if request.method=="POST":
        email = request.POST['email']        
        location = request.POST['location']
        password = request.POST['password']

        waa = WebAppAdmin.objects.filter(email=email,district=location).first()
        if waa:
            if(waa.password == password):
                return redirect("waaDashboard", unique_id = waa.unique_id) # the name id and the <str:id> should match exactky
            else:
                messages.error(request,"Invalid credentials")
                return redirect("waaLogin")
        else:
            messages.error("Account doesn't exist")
            return redirect("waaLogin")
def webAppAdminDashboard(request,unique_id):
    waa = WebAppAdmin.objects.filter(unique_id = unique_id).first()
    # print(f"{waa.district} hi")
    if not waa:
        return HttpResponse("Invalid Admin Id",status = 404)
    districts = {
        "ER":"Erode",
        "CBE":"Coimbatore",
        "TPR":"TIRUPPUR",
        "KRR":"KARUR",
        "NKL":"NAMAKKAL",
        "SLM":"SALEM"
    }
    dt = District.objects.filter(district_name = districts[waa.district]).first()
    print(f"dtid:{dt.district_id}")
    shops = Shop.objects.filter(district = dt.district_id).prefetch_related("admins")
    return render(request,"WebAppAdmin/WaaDashboard.html",
                {
                    "appAdmin":waa,
                    "shops":shops,
                }  
                )
        