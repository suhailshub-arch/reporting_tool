from django.db import models
from martor.models import MartorField
import datetime

#---------------------------- CWE ----------------------------------------

class DB_CWE(models.Model):
    cwe_id = models.IntegerField(blank=False, unique=True)
    cwe_name = models.CharField(max_length=255, blank=True)
    cwe_description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "CWEs"
    def __str__(self):
        return str(self.cwe_id)

 #---------------------------- OWASP ----------------------------------------
  
class DB_OWASP(models.Model):
    owasp_id = models.IntegerField(blank=False, unique=True)
    owasp_year = models.IntegerField(blank=False, unique=False)
    owasp_name = models.CharField(max_length=255, blank=True)
    owasp_description =  MartorField(blank=True)
    owasp_url = models.CharField(max_length=255, blank=True)
    owasp_full_id = models.CharField(max_length=20, blank=True)
 
    class Meta:
        verbose_name_plural = "OWASPs"
    def __str__(self):
        return str(self.owasp_id)
    def save(self, *args, **kwargs):
        prefix = 'A'
        if self.owasp_id < 0:
            self.owasp_full_id = "-1"
        elif self.owasp_id < 10:
            prefix += '0'
        self.owasp_full_id = prefix + str(self.owasp_id) + ':' + str(self.owasp_year)
        super().save(*args, **kwargs)


#---------------------------- Customer ----------------------------------------
          
class Customer(models.Model):
    name = models.CharField(max_length=255, blank=False)
    contact = models.EmailField(max_length=255, blank=True)
    description =  MartorField(blank=True)
    class Meta:
        verbose_name_plural = "Customers"
    def __str__(self):
        return self.name
    def get_label (self):
        return self.name


#---------------------------- Report ----------------------------------------

class Report(models.Model):
    report_id = models.CharField(max_length=255, blank=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    executive_summary_image = models.TextField(blank=True, null=True)
    owasp_categories_summary_image = models.TextField(blank=True)
    executive_summary = MartorField(blank=True)
    scope = MartorField(blank=True)
    outofscope = MartorField(blank=True)
    methodology = MartorField(blank=True)
    recommendation = MartorField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    report_date = models.DateTimeField(blank=False)
    audit_start = models.DateField(blank=True, null=True)
    audit_end = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    def get_label (self):
        return self.title
    class Meta:
        verbose_name_plural = "Reports"

#---------------------------- Finding ----------------------------------------

class Finding(models.Model):
    title = models.CharField(max_length=200, blank=True)
    finding_id = models.CharField(blank=True, max_length=200)
    status = models.CharField(max_length=200, default='Open')
    severity = models.CharField(max_length=200, blank=True)
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    cvss_vector = models.CharField(blank=True, max_length=200)
    description = MartorField(blank=True)
    location = MartorField(blank=True)
    impact = MartorField(blank=True)
    recommendation = MartorField(blank=True)
    references = MartorField(blank=True)
    poc = MartorField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    owasp =  models.ForeignKey(DB_OWASP, on_delete=models.CASCADE, null=True, blank=True)
    cwe =  models.ForeignKey(DB_CWE, on_delete=models.CASCADE, null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    def get_label (self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == "Close":
            self.closed_at = datetime.datetime.now()
        super().save(*args, **kwargs)
        
        



