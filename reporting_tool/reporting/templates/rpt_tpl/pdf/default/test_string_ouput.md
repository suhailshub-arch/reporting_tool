---
pandoc-latex-environment:
    noteblock: [note]
    tipblock: [tip]
    warningblock: [warning]
    cautionblock: [caution]
    importantblock: [important]
    tcolorbox: [box]
    info-box: [infobox]
    low-box: [lowbox]
    warning-box: [mediumbox]
    error-box: [highbox]
    critical-box: [criticalbox]
    highblock: [highnote]
    mediumblock: [mediumnote]
    lowblock: [lownote]
    infoblock: [infonote]
    debugblock: [debugnote]
    descriptionblock: [descriptionnote]
    locationblock: [locationnote]
    impactblock: [impactnote]
    recommendationblock: [recommendationnote]
    referencesblock: [referencesnote]
    additional_notesblock: [additional_notesnote]
---

## TEST FINDING CHATGPT

::: important 
**Severity**: \textcolor{criticalcolor}{Critical}

 **CVSS Score**: 11.0 

 **CVSS Vector**: rewtgergerg  
:::




**OWASP**

2 - Cryptographic Failures



**Description**

The application in question was observed using the MD5 cryptographic algorithm for hashing passwords. This algorithm is known to be deprecated and weak, making it an unsuitable choice for modern security requirements.



**Location**

https://example.com/user/settings



**Impact**

The utilization of a deprecated and weak cryptographic algorithm like MD5 makes the application highly susceptible to cyber attacks. A potential attacker can leverage well-known vulnerabilities within the MD5 algorithm to compromise user passwords, leading to unauthorized access to sensitive information.



**Proof of Concept**

TBC



**Recommendation**

- It is recommended to immediately upgrade the password hashing system to a more secure cryptographic algorithm.
- Alternatives like SHA-256 or bcrypt should be considered for password hashing.
- A thorough security review of the entire application needs should be carried out to identify and correct any other outdated security practices.



**References**

- https://owasp.org/www-project-top-ten/2021/A02_2021-Cryptographic_Failures
- https://en.wikipedia.org/wiki/MD5
- https://csrc.nist.gov/Projects/Hash-Functions/NIST-Policy-on-Hash-Functions


