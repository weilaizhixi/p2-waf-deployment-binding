# P2: Deployment binding in WAF rule validation

S1 summary analysis artifact, version **1.0.0**. Prepared for maintainer review on 2026-11-02; no GitHub upload or publication has been performed.

Related manuscript: *Rules are not guarantees: Deployment binding and its boundaries in WAF rule validation*.

This package supports inspection of selected study summaries, aggregate arithmetic checks, Wilson interval recalculation, and Markdown table generation. It is a deliberately limited research artifact. It does not reproduce the original online WAF experiments, train the B models, or reconstruct expert annotations. Publication authority and license selection remain pending; see [rights and permissions](RIGHTS_AND_PERMISSIONS.md).

## Quick start

Use a local Python installation, with no network connection required. No API keys, Docker services, or third-party Python packages are needed.

Windows PowerShell, from the extracted P2_Public_Release directory:

~~~powershell
py -B code/main.py --verify-only
py -B code/main.py
~~~

Linux/macOS:

~~~sh
python3 -B code/main.py --verify-only
python3 -B code/main.py
~~~

The second command writes six Markdown tables, summary.json, and verification.json into outputs/. An existing output with the same name is replaced. Inputs and sealed release files are not rewritten. The --verify-only command writes no files. Paths are resolved from the code location, so invoking the script from another working directory is supported. See [environment](docs/ENVIRONMENT.md) and [reproduction coverage](docs/REPRODUCIBILITY.md).

## Included material

| Material | Scope |
|---|---|
| Formal run summaries | 19 runs, 12 application clusters, 155 cells |
| Benign-task summaries | 12 applications plus a total row; 135 cells; 3 frozen-rule and 6 stock/tuned FP cells |
| Rule corpus counts | Three source groups; 6,892 rules; recorded total of 171 unique files |
| Rule frame aggregates | Directive and chain counts for F1/F2/F3, with Wilson intervals |
| B boundary aggregates | Confirmatory A01 and descriptive seven-run result tables |
| Source-layer aggregates | Six added source categories; mixed set/case/configuration/application units |

The formal HTTP-row count (1,085), benign execution count (546), and source-layer scale (22 runs / 88 cells / 672 HTTP rows) are recorded reference values. They cannot be reconstructed from raw observations in this package. The three cell counts refer to different experiments and must not be added as one sample size.

The original two approved CSVs are retained byte-for-byte. The other summaries are extracted or transcribed from existing study results. Individual labels, expert identities and returns, raw requests/responses, rules, prompts, paid-call records, credentials, and third-party source snapshots are excluded.

## Interpretation

Deployment binding means that a rule's decisive matching condition depends on a deployment-selected value rather than only attack syntax or a protocol constant. Source qualification requires an observed attack effect without the rule, blocking with the rule, successful declared benign tasks, and valid measurement with rule attribution.

- Endpoint counterexamples occurred in 19/19 formal runs; this is a run-level observation, not a population failure rate. GeoServer retains both CE and NoCE outcomes for different declared changes.
- Payload matching retained blocking in the 16 source-qualified runs under the executed changes. NoCE means no counterexample in those executed cases, not a general guarantee.
- F3 is reported as a 19-30/40 sensitivity range (47.5-75.0%), not a pooled population estimate.
- The confirmatory B comparison remains a tie: v2 model 4/4 and literal baseline 4/4. The predeclared superiority criterion was not met.
- Source-layer totals mix units; the S6 counterexample is a benign-task failure. S1-S8 are source categories, not eight independent authors.

See [method and limitations](docs/METHOD_AND_LIMITATIONS.md), [data dictionary](docs/DATA_DICTIONARY.md), and [provenance](docs/PROVENANCE.md).

## Integrity and citation

FILE_LIST.txt lists every shipped file. MANIFEST.json records payload sizes and SHA-256 hashes; it excludes itself and SHA256SUMS to avoid self-reference. SHA256SUMS covers every shipped file except itself, including MANIFEST.json. The entry point checks both inventories and hashes before analysis. Unsigned checksums establish consistency, not authorship. Generated outputs/ and Git metadata are not release payload.

Use [CITATION.bib](CITATION.bib) for a provisional artifact citation. Author names, repository URL, DOI, publication venue, and publication status have not been invented. Maintainers must confirm citation metadata and rights before public release. See [release notes](RELEASE_NOTES_v1.0.0.md).
