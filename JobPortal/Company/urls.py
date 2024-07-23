from django.urls import path
from .import views

urlpatterns = [
    # path('',views.proxy,name="proxy"),
    path('update_company',views.AddComapnyDetailsView.as_view(),name="update_company"),
    path('company_detail/<int:id>/',views.CompanyDetailsView.as_view(),name="company_detail"),
    
]
