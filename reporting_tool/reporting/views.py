from collections import Counter
import textwrap
import uuid
from django.urls import reverse
from dotenv import load_dotenv
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader
from django.template.loader import render_to_string
from .models import Finding, DB_CWE, DB_OWASP, Customer, Report
from .forms import Add_findings, AddOWASP, AddCustomer, AddReport, OWASP_Questions
from openai import OpenAI
import datetime
import pypandoc
import os
import json

#---------------------------------------------------
#                   CHATGPT
# --------------------------------------------------

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def home(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
    
#---------------------------------------------------
#                   FINDINGS
# --------------------------------------------------

def findings_open_list(request):
    findings = Finding.objects.filter(status="Open")
    template = loader.get_template('findings/findings_display.html')
    context = {
        'findings':findings,
        'status': "Open"
    }
    return HttpResponse(template.render(context, request))

def findings_closed_list(request):
    findings = Finding.objects.filter(status="Closed")
    template = loader.get_template('findings/findings_display.html')
    context = {
        'findings':findings,
        'status': "Closed"
    }
    return HttpResponse(template.render(context, request))

def add_finding(request,pk):
    report_data_json = request.session.get('report_data', None)
    # Check if report_data_json is in the session
    if report_data_json is not None:
        # Deserialize report_data_json from JSON to a dictionary
        report_data_dict = json.loads(report_data_json)
    else:
        # Handle the case where report_data is not in the session
        report_data_dict = {}
    # print(report_data)
    Report_query = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        form = Add_findings(request.POST)
        
        if form.is_valid():
            finding = form.save(commit=False) 
            finding.report = Report_query       
            finding.finding_id = uuid.uuid4()
            finding.save()
            
        return redirect('report_finding', pk=pk)
        
    else:
        form = Add_findings()
        form.fields['description'].initial = report_data_dict['description']
        form.fields['impact'].initial = report_data_dict['impact']
        form.fields['recommendation'].initial = report_data_dict['recommendation']
        form.fields['references'].initial = report_data_dict['references']
        form.fields['owasp'].initial = report_data_dict['owasp']
        form.fields['cvss_score'].initial = report_data_dict['cvss_score']
        form.fields['severity'].initial = report_data_dict['criticality']
        form.fields['status'].initial = "Open"
        template = 'findings/findings_add.html'
        context = {
            'form': form,
            'Report_query': Report_query
        }

    return render(request, template, context)

def edit_finding(request, pk):
    
    finding = get_object_or_404(Finding, pk=pk)
    Report_query = get_object_or_404(Report, pk=finding.report.id)
    
    if request.method == 'POST':
        form = Add_findings(request.POST, instance=finding)
        
        if form.is_valid():
            finding = form.save(commit=False)            
            finding.finding_id = uuid.uuid4()
            finding.save()
            
        return redirect('/findings/view/'+ str(pk))
        
    else:
        form = Add_findings(instance=finding)
        template = loader.get_template('findings/findings_add.html')
        context = {
            'form': form,
            'Report_query': Report_query
        }

    return render(request, 'findings/findings_add.html', context)

def view_finding(request, pk):
    finding = get_object_or_404(Finding, pk=pk)
    template = loader.get_template('findings/findings_view.html')
    context = {
        'finding':finding
    }
    return HttpResponse(template.render(context, request))

def finding_delete(request,pk):
    Finding.objects.filter(pk=pk).delete()
    next_url = request.GET.get('next', '/')
    return redirect(next_url)
    

#---------------------------------------------------
#                   OWASPS
# --------------------------------------------------

def owasp_list(request):
    owasps = DB_OWASP.objects.all().values()
    template = loader.get_template('owasp/owasp_list.html')
    context = {
        'owasps':owasps
    }
    return HttpResponse(template.render(context, request))

def owasp_add(request):
    if request.method == 'POST':
        form = AddOWASP(request.POST)
        
        if form.is_valid():
            owasp = form.save(commit=False)            
            owasp.save()
            
        return redirect('/owasp/list')
        
    else:
        form = AddOWASP()
        template = 'owasp/owasp_add.html'
        context = {
            'form': form
        }

    return render(request, template , context)

def owasp_edit(request,pk):
    
    owasp = get_object_or_404(DB_OWASP, pk=pk)
    
    if request.method == 'POST':
        form = AddOWASP(request.POST, instance=owasp)
        
        if form.is_valid():
            owasp = form.save(commit=False)            
            owasp.save()
            
        return redirect('/owasp/list')
        
    else:
        form = AddOWASP(instance=owasp)
        template = 'owasp/owasp_add.html'
        context = {
            'form': form
        }

    return render(request, template, context)

def owasp_delete(request,pk):
    DB_OWASP.objects.filter(pk=pk).delete()
    return redirect('/owasp/list/')

#---------------------------------------------------
#                   CUSTOMERS
# --------------------------------------------------

def customer_list(request):
    customers = Customer.objects.all()
    template = loader.get_template('customer/customer_list.html')
    context = {
        'customers':customers
    }
    return HttpResponse(template.render(context, request))

def customer_add(request):
    if request.method == 'POST':
        form = AddCustomer(request.POST)
        
        if form.is_valid():
            customer = form.save(commit=False)            
            customer.save()
            
        return redirect('/customer/list')
        
    else:
        form = AddCustomer()
        template = 'customer/customer_add.html'
        context = {
            'form': form
        }

    return render(request, template, context)

def customer_edit(request,pk):
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = AddCustomer(request.POST, instance=customer)
        
        if form.is_valid():
            customer = form.save(commit=False)            
            customer.save()
            
        return redirect('/customer/list')
    
    else:
        form = AddCustomer(instance=customer)
        template = 'customer/customer_add.html'
        context = {
            'form': form
        }

    return render(request, template, context)

def customer_delete(request,pk):
    Customer.objects.filter(pk=pk).delete()
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

def customer_view(request,pk):

    Customer_query = get_object_or_404(Customer, pk=pk)
    Report_query = Report.objects.filter(customer=Customer_query).order_by('creation_date').reverse()
    count_customer_report = Report_query.count()
    customer_findings = {}
    count_customer_findings_total = 0
    count_customer_findings_critical_high = 0
    count_customer_findings_medium = 0

    for report in Report_query:
        Finding_query = Finding.objects.filter(report=report.id)
        count_customer_findings = Finding_query.count()
        customer_findings[report.id] = count_customer_findings
        count_customer_findings_total += count_customer_findings
        for finding in Finding_query:
            if finding.severity == 'High' or finding.severity == 'Critical':
                count_customer_findings_critical_high += 1
            elif finding.severity == 'Medium':
                count_customer_findings_medium += 1

    return render(request, 'customer/customer_view.html', {'pk': pk, 'Customer_query': Customer_query, 'Report_query': Report_query, 'count_customer_report': count_customer_report, 'customer_findings': count_customer_findings_total, 'count_customer_findings_critical_high': count_customer_findings_critical_high, 'count_customer_findings_medium': count_customer_findings_medium})

#---------------------------------------------------
#                   REPORT
# --------------------------------------------------

def report_list(request):
    reports = Report.objects.all()
    template = loader.get_template('report/report_list.html')
    context = {
        'reports':reports
    }
    return HttpResponse(template.render(context, request))

def report_add(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    report_id_format = "PEN-DOC" + str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'))

    if request.method == 'POST':
        form = AddReport(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            audit_dates = request.POST['audit']
            split_audit_dates = audit_dates.split(" - ")
            report.audit_start = split_audit_dates[0]
            report.audit_end = split_audit_dates[1]
            report.save()           
            # CHANGE THIS WHEN VIEW IS DONE
            # return redirect('report/view', pk=report.pk)
            return redirect('/report/list')
    else:
        form = AddReport()
        form.fields['report_id'].initial = report_id_format
        form.fields['report_date'].initial = today
        form.fields['audit'].initial = "%s - %s" % (today,today)
        
    return render(request, 'report/report_add.html', {
        'form': form
    })

def report_edit(request,pk):

    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':
        form = AddReport(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            audit_dates = request.POST['audit']
            split_audit_dates = audit_dates.split(" - ")
            report.audit_start = split_audit_dates[0]
            report.audit_end = split_audit_dates[1]
            report.save()
            # CHANGE THIS WHEN VIEW IS DONE
            # return redirect('report/view', pk=report.pk)
            return redirect('/report/list')
    else:
        form = AddReport(instance=report)
        
    return render(request, 'report/report_add.html', {
        'form': form
    })

def report_view(request,pk):
    
    DB_report_query = get_object_or_404(Report, pk=pk)
    DB_finding_query = Finding.objects.filter(report=DB_report_query).order_by('-cvss_score')
    count_finding_query = DB_finding_query.count()


    count_findings_critical = 0
    count_findings_high = 0
    count_findings_medium = 0
    count_findings_low = 0
    count_findings_info = 0
    count_findings_none = 0

    count_open_findings = 0
    count_closed_findings = 0

    cwe_rows = []
    owasp_rows = []
    
    for finding in DB_finding_query:
        # Only reporting Critical/High/Medium/Low/Info findings
        if finding.severity == 'None':
            count_findings_none += 1
        else:

            if finding.cwe:
                finding_cwe = f"CWE-{finding.cwe.cwe_id} - {finding.cwe.cwe_name}"
                cwe_rows.append(finding_cwe)

            if finding.owasp:
                finding_owasp = f"{finding.owasp.owasp_full_id} - {finding.owasp.owasp_name}"
                owasp_rows.append(finding_owasp)

            if finding.severity == 'Critical':
                count_findings_critical += 1
            elif finding.severity == 'High':
                count_findings_high += 1
            elif finding.severity == 'Medium':
                count_findings_medium += 1
            elif finding.severity == 'Low':
                count_findings_low += 1
            elif finding.severity == 'Info':
                count_findings_info += 1


            if finding.status == 'Open':
                count_open_findings += 1
            elif finding.status == 'Closed':
                count_closed_findings += 1


    cwe_cat = Counter(cwe_rows)
    cwe_categories = []

    for key_cwe, value_cwe in cwe_cat.items():
        fixed_key_cwe = '\n'.join(key_cwe[i:i+50] for i in range(0, len(key_cwe), 50))
        dict_cwe = {
            "value": value_cwe,
            "name": fixed_key_cwe
        }
        cwe_categories.append(dict_cwe)

    owasp_cat = Counter(owasp_rows)
    owasp_categories = []

    for key_owasp, value_owasp in owasp_cat.items():
        fixed_key_owasp = '\n'.join(key_owasp[i:i+55] for i in range(0, len(key_owasp), 55))
        dict_owasp = {
            "value": value_owasp,
            "name": fixed_key_owasp
        }
        owasp_categories.append(dict_owasp)


    return render(request, 'report/report_view.html', {'DB_report_query': DB_report_query, 'DB_finding_query': DB_finding_query, 'count_finding_query': count_finding_query, 'count_findings_critical': count_findings_critical, 'count_findings_high': count_findings_high, 'count_findings_medium': count_findings_medium, 'count_findings_low': count_findings_low, 'count_findings_info': count_findings_info, 'count_findings_none': count_findings_none, 'cwe_categories': cwe_categories, 'owasp_categories': owasp_categories, 'count_open_findings': count_open_findings, 'count_closed_findings': count_closed_findings})



def report_delete(request,pk):
    Report.objects.filter(pk=pk).delete()
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

def report_finding(request,pk):
    DB_report_query = get_object_or_404(Report, pk=pk)
    DB_finding_query = Finding.objects.filter(report=DB_report_query).order_by('-cvss_score')
    
    return render(request, 'report/report_finding.html', {
        'DB_report_query' : DB_report_query,
        'DB_finding_query' : DB_finding_query,
    })
    
# ------------- PLS DELETE TESTING ----------------------

def test(request,pk):
    DB_report_query = get_object_or_404(Report, pk=pk)
    DB_finding_query = Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()
    # print(DB_finding_query[0].title)
    # for finding in  DB_finding_query:
    #     pdf_finding = render_to_string(os.path.join(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default', 'pdf_finding.md'), {'finding': finding, 'icon_finding': 'important', 'severity_color': 'criticalcolor', 'severity_color_finding': "\\textcolor{criticalcolor}{Critical}"})
        # template_findings += ''.join(pdf_finding)
    pdf_finding = render_to_string(os.path.join(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default', 'pdf_finding.html'), {'finding': DB_finding_query[0], 'icon_finding': 'important', 'severity_color': 'criticalcolor', 'severity_color_finding': "\\textcolor{criticalcolor}{Critical}"})
    print(pdf_finding)
    # pdf_finding = textwrap.dedent(pdf_finding)
    # pdf_finding = pdf_finding.encode(encoding="utf-8", errors="ignore").decode()

    output = pypandoc.convert_text(pdf_finding, to='pdf', outputfile="test.pdf", format='html',extra_args=[
                                            '-H', r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default\pdf_header.tex',
                                            '--from', 'markdown+yaml_metadata_block+raw_html',
                                            '--template', r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default\report_default.tex',
                                            '--pdf-engine', 'pdflatex',
                                            '--filter', 'pandoc-latex-environment'])
    
    with open('test.pdf', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=file.pdf'  # or 'attachment; filename=file.pdf' for download
        return response
    

def format_chatgpt_output(data):
    text = data
    # sections = ["Description:", "Impact:", "Recommendation:", "CVSS Score Number:", "Criticality:", "References:"]

    description = impact = recommendation = cvss_score = criticality = references = ""

    parts = text.split("\n\n")
    for part in parts:
        if part.startswith("Description:"):
            description = part.replace("Description:", "").strip()
        elif part.startswith("Impact:"):
            impact = part.replace("Impact:", "").strip()
        elif part.startswith("Recommendation:"):
            recommendation = part.replace("Recommendation:", "").strip()
        elif part.startswith("CVSS Score Number:"):
            cvss_score = part.replace("CVSS Score Number:", "").strip()
        elif part.startswith("Criticality:"):
            criticality = part.replace("Criticality:", "").strip()
        elif part.startswith("References:"):
            references = part.replace("References:", "").strip()

    return {
        'description': description,
        'impact': impact,
        'recommendation': recommendation,
        'cvss_score': cvss_score,
        'criticality': criticality,
        'references': references
    }
    
def test_form(request, pk):

    if request.method == 'POST':
        form = OWASP_Questions(request.POST)        
        if form.is_valid():
            DB_report_query = get_object_or_404(DB_OWASP, pk=int(form.data["owasp"]))
            info = {}
            prompt = """
Please provide content for a detailed finding report based on the above information . 
There are 6 sections to be included. 
- Description
- Impact
- Recommendation (in bullet point form)
- CVSS Score Number (assign a CVSS score based on your understanding of the vulnerability. Only include the number without any other explanation)
- Criticality (critical, high, medium, low, info only)
- References (this should include full links for reference materials). 

Ignore all HTML Tags.
            """
            str_info = ""
            for response in form:
                if response.field.label == "OWASP":
                    info[response.field.label] = DB_report_query.owasp_name
                else:
                    info[response.field.label] = response.data
            for label, value in info.items():
                temp = "{label}: {value}\n"
                str_info = str_info + temp.format(label = label, value = value)
            
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": str_info}
                ]
            )
            ai_response = completion.choices[0].message.content
            report_data = format_chatgpt_output(ai_response)
            report_data['owasp'] = form.data["owasp"]
            report_data['location'] = form.data["affected_url"]
            
            print(report_data['description'])
            report_data_json = json.dumps(report_data)
            
            request.session['report_data'] = report_data_json
            redirect_url = f'/findings/add/{pk}'
            
        return redirect(redirect_url)
        
    else:
        form = OWASP_Questions()
        template = 'test.html'
        context = {
            'form': form,
        }

    return render(request, template, context)
    
# ---------------------------------------------------------