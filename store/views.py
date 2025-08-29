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
            messages.error(request,"Account doesn't exist")
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
        
def shopCreation(request):
    if request.method=="POST":
        unique_id = request.POST['unique_id']
        admin = WebAppAdmin.objects.get(unique_id=unique_id)
        # shop_district = admin.district
        # print(f"{shop_district}")
        print("Admin dt:{admin.district}")
        districts = {
            "ER":"Erode",
            "CBE":"Coimbatore",
            "TPR":"TIRUPPUR",
            "KRR":"KARUR",
            "NKL":"NAMAKKAL",
            "SLM":"SALEM"
        }
        dist_obj = District.objects.filter(district_name = districts[admin.district]).first()
        shop_name = request.POST["shop_name"]
        shop_address = request.POST["shop_address"]
        if Shop.objects.filter(shop_name=shop_name,district=dist_obj,address=shop_address).exists():
            messages.error(request,"Shop already exists")
        else:
            Shop.objects.create(
                shop_name=shop_name,
                district=dist_obj,
                address=shop_address
            )
            messages.success(request,"Shop created successfully")
        return redirect("waaDashboard",unique_id=request.POST['unique_id'])
    return HttpResponse("Invalid request",status=400)


def shopManagement(request,shop_unique_id):
    shop = Shop.objects.filter(shop_unique_id=shop_unique_id).first()
    admins = shop.admins.all()
    return render(request,"WebAppAdmin/ShopDetails.html",{
        "shop":shop,
        "admins":admins
    })


def create_shopAdmin(request,shop_unique_id):
    shop = Shop.objects.filter(shop_unique_id=shop_unique_id).first()
    if request.method == 'POST':
        admin_name = request.POST['admin_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request,"Passwords doesnt match")
            return redirect("shopManagement",shop_unique_id=shop_unique_id)
        if ShopAdmin.objects.filter(email=email).exists():
            messages.error(request,"Email already exists!")
            return redirect("shopManagement",shop_unique_id=shop_unique_id)
        ShopAdmin.objects.create(admin_name=admin_name,email=email,password=password1,shop=shop,region=shop.district)
        messages.success(request,"Admin created successfully")
        return redirect('shopManagement',shop_unique_id=shop_unique_id)
    
def shopAdminAuth(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        region = request.POST['region']
        sa_obj = ShopAdmin.objects.filter(email=email,region=region).first()
        if sa_obj:
            if sa_obj.password == password:
                name = sa_obj.admin_name
                shop_id = sa_obj.shop.shop_unique_id 
                messages.success(request,f"Login Successfull \n Welcome {name}")
                return redirect('shopAdminDashboard',admin_id=sa_obj.admin_id)
            else :
                messages.success(request,"Incorrect password!, Please enter a valid password")
                return redirect('shopAdminAuth')
        else:
            messages.error(request,"Admin Id doesnt exist")
            return redirect('shopAdminAuth')
    return render(request,"ShopAdmin/ShopAdminLogin.html",)

def shopAdminDashboard(request,admin_id):
    sa_obj = ShopAdmin.objects.filter(admin_id=admin_id).first()
    # if not sa_obj:
    #     return HttpResponse(f"No shopAdmin with admin id = {admin_id}")
    shop_obj = sa_obj.shop
    context = {"sa_obj":sa_obj,"shop_obj":shop_obj}
    return render(request,"ShopAdmin/ShopAdminDashboard.html",context)


def sa_add_products(request,admin_id):
    return render(request,"ShopAdmin/Add_Product.html",{"admin_id":admin_id})

def productAdding(request):
    return HttpResponse("Product added")
