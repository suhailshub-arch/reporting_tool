from django.urls import path
from . import views

urlpatterns = [
    #----------------- FINDINGS -------------------------
    path('findings/findings_open_list/', views.findings_open_list, name='findings_open_list'),
    path('findings/findings_closed_list/', views.findings_closed_list, name='findings_closed_list'),
    path('findings/add/<int:pk>/', views.add_finding, name='add_finding'),
    path('findings/add_inital/<int:pk>/', views.initial_add_finding, name='initial_add_finding'),
    path('findings/view/<int:pk>', views.view_finding, name='view_finding'),
    path('findings/delete/<int:pk>', views.finding_delete, name='finding_delete'),
    path('findings/edit/<int:pk>', views.edit_finding, name='edit_finding'),

    
    #--------------------------- OWASP -------------------------    
    path('owasp/list/', views.owasp_list, name='owasp_list'),
    path('owasp/add/', views.owasp_add, name='owasp_add'),
    path('owasp/edit/<int:pk>', views.owasp_edit, name='owasp_edit'),
    path('owasp/delete/<int:pk>', views.owasp_delete, name='owasp_delete'),
    
    #------------------------ CUSTOMERS --------------------------------
    path('customer/list/', views.customer_list, name='customer_list'),
    path('customer/add/', views.customer_add, name='customer_add'),
    path('customer/edit/<int:pk>', views.customer_edit, name='customer_edit'),
    path('customer/view/<int:pk>', views.customer_view, name='customer_view'),
    path('customer/delete/<int:pk>', views.customer_delete, name='customer_delete'),
    
    #--------------------------- REPORTS --------------------------------------
    path('report/list/', views.report_list, name='report_list'),
    path('report/add/', views.report_add, name='report_add'),
    path('report/edit/<int:pk>', views.report_edit, name='report_edit'),
    path('report/view/<int:pk>', views.report_view, name='report_view'),
    path('report/delete/<int:pk>', views.report_delete, name='report_delete'),   
    path('report/finding/<int:pk>', views.report_finding, name='report_finding'),
    path('report/uploadsummaryfindings/<int:pk>', views.uploadsummaryfindings, name='uploadsummaryfindings'),
    path('report/download/pdf/<int:pk>', views.reportdownloadpdf, name='reportdownloadpdf'), 
    
    #----------------------- HOME ------------------------
    path('', views.home, name='index'),
    
    # ----------------TESTINGGG PLS DELETE ---------------------
    
    # path('form/<int:pk>', views.test_form, name='test_form'),
    # path('testing/add/finding', views.testing, name='testing'),
    # path('ajax/get_dynamic_fields', views.get_dynamic_fields, name='get_dynamic_fields'),   
    
]