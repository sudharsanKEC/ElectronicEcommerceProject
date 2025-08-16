from django.http import HttpResponse
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.rolePage,name = "role_page"),
    path("webAppAdmin-login/",views.webAppAdminLogin,name = "waaLogin"),
    path("webAppAdminValidation/",views.webAdminValidation,name = "waaValidation"),
    path("WebAppAdminDashboard/<str:id>",views.webAppAdminDashboard,name="waaDashboard")

]