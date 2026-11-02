# Third-party references

S1 vendors no third-party source code, WAF rule text, container image, paper, font, or binary. Runtime code uses only the Python standard library. Therefore no third-party package is installed by requirements.txt. This statement does not certify the ownership of project-authored code or data; see RIGHTS_AND_PERMISSIONS.md.

Study context references, without redistribution or license inference:

- [OWASP Core Rule Set](https://github.com/coreruleset/coreruleset): CRS 4.30.0; the F1/F2 labels and stock/tuned configuration context refer to this ecosystem.
- [ModSecurity](https://github.com/owasp-modsecurity/ModSecurity): recorded WAF engine v3.0.17.
- [OWASP CRS container project](https://github.com/coreruleset/modsecurity-crs-docker): the recorded study image is identified in docs/ENVIRONMENT.md, but is not required or bundled for S1.

Application names and CRS rule identifiers in summary rows identify the study context. They do not include application source code or constitute an endorsement. Community corpus snapshots, upstream license files, model prompts/outputs, and external expert rules are outside S1. Researchers seeking those materials must consult the original providers and applicable terms separately. This artifact does not claim to provide the full corpus or original experiment environment.
