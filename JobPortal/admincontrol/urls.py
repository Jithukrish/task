from django.urls import path
from .import views
from .views import UserDetailView

urlpatterns = [
    path('headersection/',views.HeaderFormView.as_view(),name="headersection"),
    path('Menubar/',views.MenuCreateView.as_view(),name="Menubar"),
    path('menu_list/',views.MenuUpdateView.as_view(),name="menu_list"),
    path('menu_list_update/<int:pk>/',views.MenuEditView.as_view(),name="menu_list_update"),
    path('menu_list_delete/<int:pk>/',views.MenuDeleteView.as_view(),name="menu_list_delete"),
    path('select_jobs/<int:user_id>/', views.SelectJobsForUserView.as_view(), name='select_jobs'),
    path('selected_jobs/<int:pk>/', UserDetailView.as_view(), name='selected_jobs'),
    path('section_first/', views.SectionView.as_view(), name='section_first'),
    path('about_us/', views.AboutUsFormView.as_view(), name='about_us'),
    path('about_img/', views.ImageView.as_view(), name='about_img'),
    path('company_logo/', views.CompanyFormView.as_view(), name='company_logo'),
    path('all_comoany_logo/', views.CompanyLogoDetailview.as_view(), name='all_comoany_logo'),
    path('company_logo_update/<int:pk>/', views.CompanyLogoUpdateView.as_view(), name='company_logo_update'),
    path('feature_section_add/', views.FeatureFormView.as_view(), name='feature_section_add'),
    path('sub_feature/', views.SubfeatureView.as_view(), name='sub_feature'),
    path('section_four/', views.TabSecondFormView.as_view(), name='section_four'),
    path('section_five/', views.TabThirdFormView.as_view(), name='section_five'),
    path('section_five_update/<int:pk>/', views.SectionFiveUpdateView.as_view(), name='section_five_update'),
    path('service_section/', views.ServiceView.as_view(), name='service_section'),
    path('service_icon/', views.ServiceiconView.as_view(), name='service_icon'),
    path('all_service/', views.ServiceAllView.as_view(), name='all_service'),
    path('service_update/<int:pk>/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('service_delete/<int:pk>/', views.ServiceDeleteView.as_view(), name='service_delete'),
    path('contact_section/', views.ContactSectionView.as_view(), name='contact_section'),
    # path('contact_section/', views.contact_section, name='contact_section'),
    path('address_section/', views.AddressView.as_view(), name='address_section'),
    path('contact_contact/', views.ContactView.as_view(), name='contact_contact'),
    path('mail_section/', views.MailView.as_view(), name='mail_section'),
    path('restrict_users/', views.RestrictUserView.as_view(), name='restrict_users'),
    path('restrict_jobs/', views.JobRestrictView.as_view(), name='restrict_jobs'),
    path('restrict_company/', views.CompanyRestrictView.as_view(), name='restrict_company'),
    path('social_media/', views.socialmediaView.as_view(), name='social_media'),
    path('social_media_list/', views.socialmediaListview.as_view(), name='social_media_list'),
    path('social_media_update/<int:pk>/', views.socialmediaUpdateView.as_view(), name='social_media_update'),
    path('social_media_delete/<int:pk>/', views.socialDeleteView.as_view(), name='social_media_delete'),
    path('advancesearch/', views.AdvancesearchView.as_view (), name='advancesearch'),
    path('admin_report/', views.AdminTotalCountJobView.as_view (), name='admin_report'),
    # path('admin_report_recent_job/', views.RecentlyPostedadminListView.as_view (), name='admin_report_recent_job'),
   
    

]
