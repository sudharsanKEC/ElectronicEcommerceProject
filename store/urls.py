from django.http import HttpResponse
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.rolePage,name = "role_page"),
    path("webAppAdmin-login/",views.webAppAdminLogin,name = "waaLogin"),
    path("webAppAdminValidation/",views.webAdminValidation,name = "waaValidation"),
    path("WebAppAdminDashboard/<str:unique_id>",views.webAppAdminDashboard,name="waaDashboard"),
    path("ShopCreation/",views.shopCreation,name="shopCreation"),
    path("shopManagement/<str:shop_unique_id>",views.shopManagement,name="shopManagement"),
    path("create_shopAdmin/<str:shop_unique_id>",views.create_shopAdmin,name = "create_shopAdmin"),
    path("shopAdminLoginPage/",views.shopAdminAuth,name="shopAdminAuth"),
    path("shopAdminDashboard/<str:admin_id>",views.shopAdminDashboard,name="shopAdminDashboard"),
    path("shopAdminProductAdd/<str:admin_id>",views.sa_add_products,name="shopAdminProductAdd"),
    path("productAdding/<str:admin_id>",views.productAdding,name="productAdding"),

    # starting customer page development
    path("customer_signup/",views.customer_signup,name="customer_signup"),
    path("customer_login/",views.customer_login,name="customer_login"),
    path("customer_dashboard/<int:id>",views.customer_dashboard,name="customer_dashboard"),
    path("customer_profile/<int:id>",views.customer_profile,name="customer_profile"),
    path("customer_orders/<int:id>",views.customer_orders,name="customer_orders"),
    path("customer_wishlist/<int:id>",views.customer_wishlist,name="customer_wishlist"),
    path("customer_logout/",views.customer_logout,name="customer_logout"),
    path("product_search/<int:id>",views.product_search,name="product_search"),
    
]