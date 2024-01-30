
## {{finding.title|safe}}

:::{{icon_finding}} 
**Severity:** {{severity_color_finding}}

{% if finding.cvss_score != "0" %}
**CVSS Score:** {{finding.cvss_score|safe}}
{% endif %}

{% if finding.cvss_vector != "0" %}
**CVSS Vector:** {{finding.cvss_vector|safe}}
{% endif %}
:::

{% if finding.cwe %}
**CWE**

{{finding.cwe.cwe_id}} - {{finding.cwe.cwe_name|safe}}
{% endif %}

{% if finding.owasp %}
**OWASP**

{{finding.owasp.owasp_id|safe}} - {{finding.owasp.owasp_name|safe}}
{% endif %}

{% if finding.description %}
**Description**

{{finding.description|safe}}
{% endif %}

{% if finding.location %}
**Location**

{{finding.location|safe}}
{% endif %}

{% if finding.impact %}
**Impact**

{{finding.impact|safe}}
{% endif %}

{% if finding.poc %}
**Proof of Concept**

{{finding.poc|safe}}
{% endif %}

{% if finding.recommendation %}
**Recommendation**

{{finding.recommendation|safe}}
{% endif %}

{% if finding.references %}
**References**

{{finding.references|safe}}
{% endif %}

