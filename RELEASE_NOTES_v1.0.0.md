# P2 S1 summary analysis artifact v1.0.0

Local candidate prepared on 2026-11-02 for maintainer review. No upload or public release has been made by the preparation process. Permissions, license selection, and final citation metadata remain pending.

This initial S1 package contains two unchanged run/application summary CSVs, four extracted/transcribed aggregate CSVs, a reference JSON file, offline Python checks, and Markdown table generation. It reports the existing results without rerunning or changing the original experiments.

Preserved conclusions include 19/19 endpoint counterexample runs, 16/16 source-qualified payload runs with no counterexample in executed cases, benign totals of 135 cells with 3 frozen-rule and 6 stock/tuned failures, the F3 sensitivity range, and the unmet B superiority criterion (4/4 versus 4/4).

Expert records and identities, raw requests/responses, full rule corpora, third-party source snapshots, model/API records, and manuscripts are excluded. See docs/REPRODUCIBILITY.md for the limited scope of reproducibility. Code validation was performed on CPython 3.14.6 / Windows 10, with no third-party dependencies or network services.

The separately supplied P2_Public_Release_v1.0.0.zip is the curated artifact archive. Its adjacent .sha256 file checks the ZIP bytes. FILE_LIST.txt, MANIFEST.json, and SHA256SUMS describe the extracted public directory. GitHub-generated source archives are separate assets and will have different byte-level hashes.
