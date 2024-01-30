# ----------  Template filters ------------

from django import template
from reporting.models import Report, Finding

import json

register = template.Library()

@register.filter('findings_count')
def findings_count(reports):
    """
    usage example {{ value1|findings_count }}
    """
    count_findings = 0

    for r in reports:
        count_report_findings = Finding.objects.filter(report=r.id).count()
        count_findings = count_findings + count_report_findings

    return count_findings