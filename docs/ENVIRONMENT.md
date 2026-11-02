# Environment

The S1 analysis uses the Python standard library only: argparse, csv, hashlib, json, math, pathlib, and sys. requirements.txt intentionally lists no installable packages. There is no package download, API request, model invocation, container startup, or database access in the public code.

The code targets CPython 3.10 or later. Actual validation was performed on CPython 3.14.6, 64-bit Windows 10 (build 19045). Other Python versions and operating systems have not been executed in this preparation. Use -B to avoid generating bytecode caches. Data are UTF-8 CSV/JSON; the two unchanged original CSVs use CRLF line endings and are read with newline-aware CSV parsing.

The original online study recorded ModSecurity v3.0.17 with an nginx connector and image owasp/modsecurity-crs:4.30.0-nginx-202610051210. The stock configuration used CRS 4.30.0 and BLOCKING_PARANOIA=1; other detection/anomaly settings used image defaults. Custom frozen-rule arms did not include stock CRS. Response-body inspection was enabled only for response-content arms. These historical settings are context, not dependencies for S1 or a complete environment lock.

The private B analysis recorded Python 3.12.13, NumPy 2.5.4, and scikit-learn 1.7.2, without a complete original lockfile. S1 neither installs those versions nor reruns B training. The formal runner evolved across runs; a single historical runner version cannot be claimed for all 19 runs. This release does not provide an online experiment runner, container digests, or a full original execution environment.
