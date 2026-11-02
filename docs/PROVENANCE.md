# Provenance and public-code changes

The approved scope is S1. No original project files were edited. The public code is a summary-only adaptation of the P2 workspace analysis code, not the original experimental runner. It retains the Wilson constant/formula and relevant counting/table logic; it replaces private-document parsing with explicit public CSV/JSON schemas, removes individual-label and agreement processing, and adds inventory verification and output-directory controls.

| Released input | Source | Transformation |
|---|---|---|
| p2_formal_runs_19.csv | Approved workspace/data file | None; identical bytes |
| p2_benign_suite_12apps.csv | Approved workspace/data file | None; identical bytes |
| p2_rule_corpus_summary.csv | Existing result anchor, section A | Extract counts, normalize numeric formatting, state file-count basis |
| p2_rule_frame_summary.csv | Existing result anchor, sections B and C1 | Extract group counts and intervals only; omit individuals and C2 responses |
| p2_b_boundary_summary.csv | Existing result anchor, section L | Transcribe L.2 confirmatory and seven-run descriptive counts; omit post-hoc records |
| p2_source_layer_summary.csv | Existing result anchor, section K | Transcribe six source-layer category totals; retain differing units and S6 benign scope |
| reported_summary.json | Existing result anchor, sections A/B/C/G/J/K/L | Selected reference values and interpretation; no new measurements |

The internal result anchor is the existing 05 results document, not redistributed. Its SHA-256 at preparation was d3d8d4bd4f8ed4fb245ec3c63a66b68f8303ef62141324e317425c17ecff3182. Local source-to-release comparison evidence is outside the public upload tree. This digest identifies the consulted snapshot and does not establish its public availability.

No source rule, third-party code, author PDF, raw run log, model response, or individual expert record was copied into the release. No new result is inserted into any original experiment. The related manuscript title is taken from the locally revised English document; the manuscript itself is excluded. Author list, repository URL, DOI, and publication status require maintainer confirmation.
