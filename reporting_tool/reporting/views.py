
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseServerError, JsonResponse
from django.template import loader
from django.template.loader import render_to_string
from django.core.files.base import ContentFile


from .models import Finding, DB_CWE, DB_OWASP, Customer, Report


from .forms import Add_findings, AddOWASP, AddCustomer, AddReport, OWASP_Questions


from dotenv import load_dotenv
from collections import Counter
from time import sleep
from openai import OpenAI
import datetime
import pypandoc
import os
import json
import base64
import pathlib
import textwrap
import uuid

#---------------------------------------------------
#                   CHATGPT
# --------------------------------------------------

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def format_chatgpt_output(ai_response, form):
    ai_response = ai_response.replace("'", '"')
    report_data = json.loads(ai_response)
    if type(report_data['References']) is not str:
        for index, reference in enumerate(report_data['References']):
            if reference[0] != "-":
                report_data['References'][index] = "- " + reference
        report_data['References'] = "\n".join(report_data['References'])
        
    if type(report_data['Recommendation']) is not str:
        for index, recommendation in enumerate(report_data['Recommendation']):
            if recommendation[0] != "-":
                report_data['Recommendation'][index] = "- " + recommendation
        
        report_data['Recommendation'] = "\n".join(report_data['Recommendation'])
    

    report_data['owasp'] = form.data["owasp"]
    report_data['location'] = form.data["affected_url"]
    return report_data

#---------------------------------------------------
#                   HOME
# --------------------------------------------------

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
        form.fields['description'].initial = report_data_dict['Description']
        form.fields['impact'].initial = report_data_dict['Impact']
        form.fields['recommendation'].initial = report_data_dict['Recommendation']
        form.fields['references'].initial = report_data_dict['References']
        form.fields['owasp'].initial = report_data_dict['owasp']
        form.fields['cvss_score'].initial = report_data_dict['CVSS Score Number']
        form.fields['severity'].initial = report_data_dict['Criticality']
        form.fields['location'].initial = report_data_dict['location']
        form.fields['status'].initial = "Open"
        form.fields['poc'].initial = "TBC"
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

def initial_add_finding(request, pk):

    if request.method == 'POST':
        form = OWASP_Questions(request.POST)        
        if form.is_valid():
            DB_owasp_query = get_object_or_404(DB_OWASP, pk=int(form.data["owasp"]))
            info = {}
            prompt = """
You are a professional penetration tester. You have performed a penetration test on a particular company. You will provided details on a particular vulnerability that was found during the penetration test. 
Please provide content for a detailed finding report based on the information that will be given. The report will be included as part of the complete penetration testing report.
There are 6 sections to be included. 
- Description
- Impact
- Recommendation (in bullet point form)
- CVSS Score Number (assign a CVSS score based on your understanding of the vulnerability. Only include the number without any other explanation)
- Criticality (critical, high, medium, low, info only)
- References (this should include full links for reference materials.). 

Ignore all HTML Tags. Output in JSON Format with each Section header, eg Description, Impact as keys. Do not include any newline characters in the response.
            """
            str_info = ""
            for response in form:
                if response.field.label == "OWASP":
                    info[response.field.label] = "%s : %s" %(DB_owasp_query.owasp_full_id , DB_owasp_query.owasp_name)
                else:
                    info[response.field.label] = response.data
            for label, value in info.items():
                temp = "{label}: {value}\n"
                str_info = str_info + temp.format(label = label, value = value)
            
            while True:
                try:
                    completion = client.chat.completions.create(
                        model="gpt-4",
                        # model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": str_info}
                        ]
                    )
                    ai_response = completion.choices[0].message.content
                    
                    report_data = format_chatgpt_output(ai_response,form)
                    break
                except json.JSONDecodeError:
                    sleep(0.5)
            
            
            report_data_json = json.dumps(report_data)
            
            request.session['report_data'] = report_data_json
            redirect_url = f'/findings/add/{pk}'
            
        return redirect(redirect_url)
        
    else:
        form = OWASP_Questions()
        template = 'findings/findings_initital_add.html'
        context = {
            'form': form,
        }

    return render(request, template, context)
    

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
    

def uploadsummaryfindings(request, pk):
    DB_report_query = get_object_or_404(Report, pk=pk)

    if request.method == 'POST':

        # Severitybar
        summary_finding_file_base64 = request.POST['fileSeveritybar']
        format, summary_finding_file_str = summary_finding_file_base64.split(';base64,')
        summary_ext = format.split('/')[-1]
        dataimgSeveritybar = ContentFile(base64.b64decode(summary_finding_file_str))

         # OWASP Categories
        owasp_summary_categories_file_base64 = request.POST['file_owasp']
        formatf, owasp_summary_categories_finding_file_str = owasp_summary_categories_file_base64.split(';base64,')
        owasp_ext = formatf.split('/')[-1]
        dataOWASP = ContentFile(base64.b64decode(owasp_summary_categories_finding_file_str))

        DB_report_query.executive_summary_image = summary_finding_file_base64
        DB_report_query.owasp_categories_summary_image = owasp_summary_categories_file_base64
        DB_report_query.save()

        return HttpResponse('{"status":"success"}', content_type='application/json')
    else:
        return HttpResponseServerError('{"status":"fail"}', content_type='application/json')


def reportdownloadpdf(request,pk):
    DB_report_query = get_object_or_404(Report, pk=pk)
    DB_finding_query = Finding.objects.filter(report=DB_report_query).order_by('cvss_score').reverse()

    # ------------------------------------------------------------------------------------------------------------------------------------------------------    

    # Datetime
    now = datetime.datetime.utcnow()
    report_date = DB_report_query.report_date.strftime('%d-%m-%Y')

    # PDF filename
    file_name = 'PEN_PDF' + '_' + DB_report_query.title + '_' +  str(datetime.datetime.utcnow().strftime('%Y%m%d%H%M')).replace('/', '') + '.pdf'

    # INIT
    template_findings = template_appendix = pdf_finding_summary = ''
    md_author = 'Shub'
    md_subject = 'PDF REPORT'
    md_website = 'https//:www.shub_pentest.com'
    
    # IMAGES
    report_executive_summary_image = DB_report_query.executive_summary_image
    report_owasp_categories_image = DB_report_query.owasp_categories_summary_image
    
    counter_finding = counter_finding_critical = counter_finding_high = counter_finding_medium = counter_finding_low = counter_finding_info = 0

    for finding in DB_finding_query:


        # Only reporting Critical/High/Medium/Low/Info findings
        if finding.severity == 'None':
            pass
        else:
            counter_finding += 1

            if finding.severity == 'Critical':
                counter_finding_critical += 1
                icon_finding = 'important'
                severity_color = 'criticalcolor'
                severity_box = 'criticalbox'
            elif finding.severity == 'High':
                counter_finding_high += 1
                icon_finding = 'highnote'
                severity_color = 'highcolor'
                severity_box = 'highbox'
            elif finding.severity == 'Medium':
                counter_finding_medium += 1
                icon_finding = 'mediumnote'
                severity_color = 'mediumcolor'
                severity_box = 'mediumbox'
            elif finding.severity == 'Low':
                counter_finding_low += 1
                icon_finding = 'lownote'
                severity_color = 'lowcolor'
                severity_box = 'lowbox'
            else:
                counter_finding_info += 1
                icon_finding = 'debugnote'
                severity_color = 'debugcolor'
                severity_box = 'infobox'

            pdf_finding_summary += render_to_string(os.path.join(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default', 'pdf_finding_summary.md'),{'finding': finding,'counter_finding': counter_finding, 'severity_box': severity_box})
            severity_color_finding = "\\textcolor{" + f"{severity_color}" +"}{" + f"{finding.severity}" + "}"

            # finding
            pdf_finding = render_to_string(os.path.join(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default', 'pdf_finding.md'), {'finding': finding, 'icon_finding': icon_finding, 'severity_color': severity_color, 'severity_color_finding': severity_color_finding })
            template_findings += ''.join(pdf_finding)

    pdf_markdown_report = render_to_string(os.path.join(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default', 'pdf_header.yaml'), {'DB_report_query': DB_report_query, 'md_author': md_author, 'report_date': report_date, 'md_subject': md_subject, 'md_website': md_website, 'report_pdf_language': 'en', 'titlepagecolor': 'e6e2e2', 'titlepagetextcolor': "000000", 'titlerulecolor': "cc0000", 'titlepageruleheight': 2 })
    pdf_markdown_report += render_to_string(os.path.join(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default', 'pdf_report.md'), {'DB_report_query': DB_report_query, 'template_findings': template_findings, 'report_executive_summary_image': report_executive_summary_image, 'report_owasp_categories_image': report_owasp_categories_image, 'pdf_finding_summary': pdf_finding_summary})

    final_markdown = textwrap.dedent(pdf_markdown_report)

    
    
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
   
    # pdf_finding = render_to_string(os.path.join(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default', 'pdf_finding.md'), {'finding': DB_finding_query[0], 'icon_finding': 'highblock', 'severity_color': 'criticalcolor', 'severity_color_finding': "\\textcolor{criticalcolor}{Critical}"})
    # pdf_finding = pdf_finding.encode(encoding="utf-8", errors="ignore").decode()
    # final_markdown = textwrap.dedent(pdf_markdown_report)
    header = render_to_string(r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default\pdf_header.yaml')
    final_markdown = header + final_markdown 
    
    pypandoc.convert_text(final_markdown, to='pdf', outputfile="test.pdf", format='md',extra_args=[
                                        '-H', r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default\pdf_header.tex',
                                        '--filter', 'pandoc-latex-environment',
                                        '--from', 'markdown+yaml_metadata_block+raw_html',
                                        '--template', r'C:\Users\USER\Third Year Project\reporting_tool\reporting\templates\rpt_tpl\pdf\default\report_default.tex',
                                        '--pdf-engine', 'pdflatex',])
    with open('test.pdf', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + file_name  # or 'attachment/inline; filename=file.pdf' 
        return response
    