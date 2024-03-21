import os


USER_CONFIG = {
    "default_admin_username" : "admin",
    "default_admin_password" : "adminpassword",
    "default_admin_email" : "admin@example.com",
}

DJANGO_CONFIG = {
    'secret_key': os.getenv("SECRET_KEY", default="django-insecure-7j2a!2kaa*a1w)#_rgf&b_)if39-6n4(a1brv51lgu@h(zm8x8"),
    'debug': int(os.getenv("DEBUG", default=0)),
    'allowed_hosts': os.getenv("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(","),
    'csrf_trusted_origins':  os.getenv("CSRF_TRUSTED_ORIGIN", default='http://localhost,http://127.0.0.1').split(","),
    'time_zone': 'UTC'
}

DELIVERABLES_CONFIG = {
    'md_author' : "Admin",
    'md_subject' : "Report Subject",
    'md_website': "admin@example.com",
    'report_id_format': 'PEN-DOC-',
    'report_pdf_name': 'PEN-PDF',
    'report_excel_name': 'PEN-EXCEL',
    'initial_text': 'TBC',
    'titlepage-color': 'e6e2e2',
    'titlepage-text-color': "000000",
    'titlepage-rule-color': "cc0000",
    'titlepage-rule-height': 2,
    'pdf_engine': 'pdflatex' # pdflatex or xelatex
}