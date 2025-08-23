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
]