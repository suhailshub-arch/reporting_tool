from django import forms
from django.forms import Textarea, TextInput, DateInput, ModelChoiceField, EmailField, BooleanField, FileInput
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from .models import DB_CWE, DB_OWASP, Customer, Report, Finding
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
    # cwe = CWEModelChoiceField(queryset=DB_CWE.objects.all(), empty_label=("(Select a CWE)"), widget=forms.Select(attrs={'class': 'form-control select2CWE'}))
    owasp = OWASPModelChoiceField(queryset=DB_OWASP.objects.all(), empty_label=("(Select an OWASP ID)"), widget=forms.Select(attrs={'class': 'form-control select2OWASP'}))
    description = SummernoteTextField()
    location = SummernoteTextField()
    poc = SummernoteTextField()
    impact = SummernoteTextField()
    recommendation = SummernoteTextField()
    references = SummernoteTextField()

    class Meta:
        model = Finding
        fields = ('title', 'status', 'severity', 'cvss_score', 'cvss_vector', 'description', 'location', 'poc', 'impact', 'recommendation', 'references', 'owasp')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Finding title")}),
            'cvss_vector': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("CVSS Vector")}),
            'cvss_score': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("CVSS Score"),}),
            'description': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'location': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'poc': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'impact': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'recommendation': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'references': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
           }
    
    
class AddOWASP(forms.ModelForm):
    
    owasp_description = SummernoteTextField()
    
    class Meta:
        model = DB_OWASP
        fields = ('owasp_id', 'owasp_year', 'owasp_name', 'owasp_description', 'owasp_url')

        widgets = {
            'owasp_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': "OWASP ID"}),
            'owasp_year': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP Year")}),
            'owasp_name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP Name")}),
            'owasp_description': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP Description")}),
            'owasp_url': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("OWASP URL")}),
        }
        
        
class AddCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'description', 'contact')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Name")}),
            'description': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Description")}),
            'contact': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ("Contact")}),
        }
    
        
class AddReport(forms.ModelForm):

    customer_placeholder = ('(Select a customer)')
    customer = CustomModelChoiceField(queryset=Customer.objects.all(), empty_label=customer_placeholder, widget=forms.Select(attrs={'class': 'form-control'}))
    audit = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control float-right', 'data-toggle': 'datetimepicker', 'data-target': '#audit', 'data-date-format': 'YYYY-MM-DD', 'id': "audit"}))
    executive_summary = SummernoteTextField()
    scope = SummernoteTextField()
    methodology = SummernoteTextField()
    outofscope = SummernoteTextField()
    recommendation = SummernoteTextField()
    
    class Meta:
        today = datetime.date.today().strftime('%Y-%m-%d')
        nowformat = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        model = Report
        fields = ('customer', 'report_id', 'title', 'report_date', 'executive_summary', 'scope', 'outofscope', 'methodology', 'recommendation', 'audit')

        widgets = {
            'report_id': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'title': TextInput(attrs={'class': 'form-control', 'type': "text", 'required': "required", 'placeholder': ('Report Name')}),
            'executive_summary': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'scope': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'outofscope': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'methodology': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'recommendation': SummernoteWidget(attrs={'class': 'form-control', 'type': "text", 'required': "required"}),
            'report_date': TextInput(attrs={'class': 'form-control datetimepicker-input', 'type': "text", 'data-toggle': 'datetimepicker', 'data-target': '#reportdate', 'data-date-format': 'YYYY-MM-DD', 'id': "reportdate", 'required': "required"}),
        }