from django import forms
from django.forms import Textarea, TextInput, DateInput, ModelChoiceField, EmailField, BooleanField, FileInput
from django.contrib.auth.models import User
from .models import DB_CWE, DB_OWASP, Customer, Report, Finding, Finding_Template, UserProfile, Appendix
from martor.fields import MartorFormField
from martor.widgets import MartorWidget
import datetime

class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name
    
class OWASPModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.owasp_full_id, obj.owasp_name)
    
class CWEModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.cwe_id, obj.cwe_name)
    
class ReportModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.title)
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
        

class Add_findings(forms.ModelForm):
    
    severity_choices = (
        ('', ('(Select severity)')),
        ('Critical', ('Critical')),
        ('High', ('High')),
        ('Medium', ('Medium')),
        ('Low', ('Low')),
        ('Info', ('Info')),
        ('None', ('None')),
    )

    status_choices = (
        ('', ('(Select status)')),
        ('Open', ('Open')),
        ('Closed', ('Closed')),
    )

    severity = forms.ChoiceField(choices=severity_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Critical/High/Medium/Low/Info/None")}))
    status = forms.ChoiceField(choices=status_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Open/Close")}))
    owasp = OWASPModelChoiceField(queryset=DB_OWASP.objects.all(), empty_label=("(Select an OWASP ID)"), widget=forms.Select(attrs={'class': 'form-control select2OWASP'}))

    class Meta:
        model = Finding
        fields = ('title', 'status', 'severity', 'cvss_score', 'cvss_vector', 'description', 'location', 'poc', 'recommendation', 'references', 'owasp')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Finding title")}),
            'cvss_vector': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("CVSS Vector")}),
            'cvss_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("CVSS Score"),}),
            'description': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'location': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'poc': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            # 'impact': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'recommendation': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'references': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
           }
    
class NewFindingTemplateForm(forms.ModelForm):

    severity_choices = (
        ('', ('(Select severity)')),
        ('Critical', ('Critical')),
        ('High', ('High')),
        ('Medium', ('Medium')),
        ('Low', ('Low')),
        ('Info', ('Info')),
        ('None', ('None')),
    )

    severity = forms.ChoiceField(choices=severity_choices, required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Critical/High/Medium/Low/Info/None")}))
    
    owasp = OWASPModelChoiceField(queryset=DB_OWASP.objects.all(), empty_label=("(Select an OWASP ID)"), widget=forms.Select(attrs={'class': 'form-control select2OWASP'}))

    class Meta:
        model = Finding_Template
        fields = ('title', 'severity', 'cvss_score', 'cvss_vector', 'description', 'recommendation', 'references', 'owasp')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Finding title")}),
            'cvss_vector': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("CVSS Vector")}),
            'cvss_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("CVSS Score"),}),
           }
        
class AddOWASP(forms.ModelForm):    
    
    class Meta:
        model = DB_OWASP
        fields = ('owasp_id', 'owasp_year', 'owasp_name', 'owasp_description', 'owasp_url')

        widgets = {
            'owasp_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "OWASP ID"}),
            'owasp_year': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP Year")}),
            'owasp_name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP Name")}),
            'owasp_description': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP Description")}),
            'owasp_url': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP URL")}),
        }
        
        
class AddCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'description', 'contact')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Name")}),
            'contact': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Contact")}),
        }
    
        
class AddReport(forms.ModelForm):

    customer_placeholder = ('(Select a customer)')
    customer = CustomModelChoiceField(queryset=Customer.objects.all(), empty_label=customer_placeholder, widget=forms.Select(attrs={'class': 'form-control'}))
    audit = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control float-right', 'data-toggle': 'datetimepicker', 'data-target': '#audit', 'data-date-format': 'YYYY-MM-DD', 'id': "audit"}))
    
    class Meta:
        today = datetime.date.today().strftime('%Y-%m-%d')
        nowformat = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        model = Report
        fields = ('customer', 'report_id', 'title', 'report_date', 'executive_summary', 'scope', 'outofscope', 'methodology', 'recommendation', 'audit')

        widgets = {
            'report_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ('Report Name')}),
            'executive_summary': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'scope': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'outofscope': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'methodology': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'recommendation': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'report_date': TextInput(attrs={'class': 'form-control datetimepicker-input', 'type': "text", 'data-toggle': 'datetimepicker', 'data-target': '#reportdate', 'data-date-format': 'YYYY-MM-DD', 'id': "reportdate", 'required': "required"}),
        }
        
    
class OWASP_Questions(forms.Form):
    
    severity_choices = (
        ('', ('(Select severity)')),
        ('Critical', ('Critical')),
        ('High', ('High')),
        ('Medium', ('Medium')),
        ('Low', ('Low')),
        ('Info', ('Info')),
        ('None', ('None')),
    )
    
    owasp = OWASPModelChoiceField(queryset=DB_OWASP.objects.all(), label="OWASP", empty_label=("(Select an OWASP ID)"), widget=forms.Select(attrs={'class': 'form-control select2OWASP', 'id': 'id_owasp'}))
    affected_url = MartorFormField( label="Affected URL")
    severity = forms.ChoiceField(choices=severity_choices, label="Severity", required=True, widget=forms.Select(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Critical/High/Medium/Low/Info/None")}))

    # Broken Access Control Fields
    unauthorized_actions = MartorFormField( label="Data Exposed", required=False)
    access_control_flaw = MartorFormField( label="Data Exposed", required=False)
    
    # Cryptographic Fields
    data_exposed = MartorFormField( label="Data Exposed", required=False)
    encryption_issue = MartorFormField( label="Encryption Issue", required=False)
    
    # Injection Fields
    injection_type = MartorFormField( label="Injection Type", required=False)
    injection_input = MartorFormField( label="Injection Input", required=False)
    
    # Insecure Design
    design_flaw = MartorFormField( label="Data Exposed", required=False)
    affected_component = MartorFormField( label="Data Exposed", required=False)
    
    # Security Misconfiguration
    misconfigured_element = MartorFormField( label="Data Exposed", required=False)
    configuration_flaw = MartorFormField( label="Data Exposed", required=False)
    
    # Vulnerable and Outdated Components
    component_name = MartorFormField( label="Data Exposed", required=False)
    component_version = MartorFormField( label="Data Exposed", required=False)
    
    # Identification and Authentication Failure
    authentication_issue = MartorFormField( label="Data Exposed", required=False)
    impact_of_issue = MartorFormField( label="Data Exposed", required=False)
    
    # Software and Data Integrity Failure
    integrity_issue = MartorFormField( label="Data Exposed", required=False)
    source_of_issue = MartorFormField( label="Data Exposed", required=False)
    
    # Security Logging and Monitoring Failures
    logging_flaw = MartorFormField( label="Data Exposed", required=False)
    detection_issue = MartorFormField( label="Data Exposed", required=False)
    
    # SSRF
    trigger_point = MartorFormField( label="Data Exposed", required=False)
    ssrf_impact = MartorFormField( label="Data Exposed", required=False)
    
    
class UploadNmapForm(forms.Form):
    nmap_file = forms.FileField()

    
class UploadOpenVASForm(forms.Form):
    openvas_file = forms.FileField(required=True)


class FindingModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"({obj.report.title}) - {obj.title}"


class AppendixForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        reportpk = kwargs.pop('reportpk')
        super(AppendixForm, self).__init__(*args, **kwargs)

        finding_query = Finding.objects.filter(report=reportpk)

        self.fields["finding"] = FindingModelChoiceField(queryset=finding_query, empty_label=("(Select a finding)"), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Appendix
        fields = ('finding', 'title', 'description' )

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Title")}),
        }