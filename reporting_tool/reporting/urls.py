from django.urls import path
from . import views

urlpatterns = [
    # ----------------- AUTH -----------------------------
    path('accounts/password_change/', views.CustomPasswordChangeView.as_view(), name='custom_password_change'),
    path('accounts/password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='custom_password_change_done'),  
    
    # ----------------- USER ---------------------------------
    path('view_profile/', views.user_view, name='user_view'),
    path('edit_profile/', views.user_edit, name='user_edit'),
    
    #----------------- FINDINGS -------------------------
    path('findings/findings_open_list/', views.findings_open_list, name='findings_open_list'),
    path('findings/findings_closed_list/', views.findings_closed_list, name='findings_closed_list'),
    path('findings/add/<int:pk>/', views.add_finding, name='add_finding'),
    path('findings/add_inital/<int:pk>/', views.initial_add_finding, name='initial_add_finding'),
    path('findings/view/<int:pk>', views.view_finding, name='view_finding'),
    path('findings/delete/<int:pk>', views.finding_delete, name='finding_delete'),
    path('findings/edit/<int:pk>', views.edit_finding, name='edit_finding'),

    #----------------- TEMPLATES -------------------------
    path('template/list/', views.template_list, name='template_list'),
    path('template/add/', views.template_add, name='template_add'),
    path('template/edit/<int:pk>', views.template_edit, name='template_edit'),
    path('template/delete/<int:pk>', views.template_delete, name='template_delete'),
    path('template/view/<int:pk>', views.template_view, name='template_view'),
    path('template/add/finding/<int:pk>', views.templateaddfinding, name='templateaddfinding'),
    path('template/add/report/<int:pk>/<int:reportpk>', views.templateaddreport, name='templateaddreport'),
    
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
    
    # ----------------------- SETTINGS -------------------------------------------
    path('settings', views.settings, name='settings'),
    # path('update_font_size/', views.update_font_size, name='update_font_size'),
    # path('update_background_color/', views.update_background_colour, name='update_background_colour'),
    # path('update_font_color/', views.update_font_colour, name='update_font_colour'),
    # path('update_font_type/', views.update_font_type, name='update_font_type'),
    # path('update_character_spacing/', views.update_character_spacing, name='update_character_spacing'),
    path('update_preference/', views.update_preference, name='update_preference'),

    
    #----------------------- HOME ------------------------
    path('', views.home, name='home'),
    
    # ----------------TESTINGGG PLS DELETE ---------------------
    
    # path('form/<int:pk>', views.test_form, name='test_form'),
    # path('testing/add/finding', views.testing, name='testing'),
    # path('ajax/get_dynamic_fields', views.get_dynamic_fields, name='get_dynamic_fields'),   
    
]