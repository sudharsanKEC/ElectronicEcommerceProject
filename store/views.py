import uuid
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.db.models import Q
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
    if not sa_obj:
        return HttpResponse(f"No shopAdmin with admin id = {admin_id}")
    shop_obj = sa_obj.shop
    context = {"sa_obj":sa_obj,"shop_obj":shop_obj}
    return render(request,"ShopAdmin/ShopAdminDashboard.html",context)


def sa_add_products(request,admin_id):
    return render(request,"ShopAdmin/Add_Product.html",{"admin_id":admin_id})

def productAdding(request,admin_id):
    if request.method == "POST":
        shop = ShopAdmin.objects.filter(admin_id=admin_id).first().shop
        category = request.POST["category"]
        name = request.POST["productName"]
        cost = request.POST['cost']
        description = request.POST['description']
        stock_quantity = int(request.POST['stock_quantity'])  # convert to int
        image = request.FILES['product_image']

        # Loop for quantity and create unique products
        for i in range(stock_quantity):
            unique_id = str(uuid.uuid4())  # generates a unique ID
            Product.objects.create(
                shop=shop,
                category=category,
                name=name,
                cost=cost,
                description=description,
                product_unique_id=unique_id,  # assuming you added this field
                image=image
            )

        messages.success(request, f"{stock_quantity} product(s) added successfully to the inventory")
        return redirect("productAdding", admin_id=admin_id)

    return render(request, "ShopAdmin/Add_Product.html", {"admin_id": admin_id})


def customer_signup(request):
    if request.method=="POST":
        name = request.POST["user-name"]
        mail = request.POST['user-mail']
        mobile_no = request.POST['mobile-no']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        region = request.POST['region']
        resident = request.POST['resident']
        if Customer.objects.filter(email=mail).exists():
            messages.error(request,"User already exists with this email ID")
            return redirect("customer_signup")
        elif pass1!=pass2:
            messages.error(request,"Passwords doesnt match each other")
            return redirect("customer_signup")
        else:
            customer = Customer.objects.create(name=name,email=mail,password=pass1,region=region,phone_number=mobile_no,residential_place=resident)
            messages.success(request,"Customer account created successfully")
            return redirect("customer_dashboard",id=customer.id)

    return render(request,"Customer/Customer_signup.html")

def customer_login(request):
    if request.method == "POST":
        email = request.POST["mail"]
        password = request.POST["password"]
        customer = Customer.objects.filter(email=email).first()
        if customer:
            if customer.password == password:
                messages.success(request,"Login successfull")
                return redirect("customer_dashboard",id=customer.id)
            else:
                messages.error(request,"Incorrect password")
                return redirect("customer_login")
        else:
            messages.error(request,"No account found for the given mail ID")
            return redirect("customer_login")
    return render(request,"Customer/customer_login.html")
def customer_dashboard(request,id):
    customer = get_object_or_404(Customer, id=id)
    products = Product.objects.all()
    return render(request,"Customer/Customer_dashboard.html",{"customer":customer,"products":products})

def customer_profile(request,id):
    return HttpResponse("Customer profile page")

def customer_orders(request,id):
    return HttpResponse("Placed orders")

def customer_wishlist(request,id):
    return HttpResponse("Items in cart")

def customer_logout(request):
    return HttpResponse("Log out page")

def product_search(request,id):
    query = request.GET.get("q", "")
    products = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    customer = get_object_or_404(Customer, id=id)
    return render(request, "Customer/search_results.html", {
        "query": query,
        "products": products,
        "customer":customer
    })

def customer_profile(request,id):
    customer = Customer.objects.filter(id=id).first()
    return render(request,"Customer/customer_profile.html",{"customer":customer})
