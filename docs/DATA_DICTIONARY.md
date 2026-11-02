# Data dictionary

All tables use a header row. Integer counts are nonnegative. Boolean-like fields in the original formal CSV use the strings true, false, and none; none is an absent arm, not false. FP counts refer to cells, not requests or execution-level false-positive rates. No row is an individual expert response.

## p2_formal_runs_19.csv

Nineteen original summary rows, copied byte-for-byte.

| Field | Meaning |
|---|---|
| run | Historical experiment identifier; not a hostname or account ID |
| sample | Application/task sample; the explicit cluster map is in code/verify.py |
| cells | Executed test cells for this run |
| endpoint_source_qualified | Source qualification for the endpoint arm |
| payload_source_qualified | Source qualification for the payload arm; none means absent |
| stock_source_qualified | Source qualification for stock CRS |
| endpoint_outcomes / payload_outcomes / stock_outcomes | Outcome token(s); a semicolon preserves different declared changes |
| vulnerability_family | Recorded effect-family description; 18 distinct strings |

COUNTEREXAMPLE (CE) means an observed counterexample under an executed deployment change. NO_COUNTEREXAMPLE_IN_EXECUTED_CASE (NoCE) is limited to the executed cases. SOURCE_INELIGIBLE_OR_TARGET_NOT_INSTANTIATED does not establish successful target protection. Empty payload outcomes accompany absent payload arms. The GeoServer endpoint row includes both CE and NoCE; neither may be discarded.

bWAPP tasks map to one bWAPP cluster. minio_response maps to MinIO, nodered_adminread to Node-RED, and pocketbase_file to PocketBase. Therefore 19 runs represent 12 application clusters.

## p2_benign_suite_12apps.csv

Twelve application rows and one TOTAL row, copied byte-for-byte.

| Field | Meaning |
|---|---|
| application | Application cluster, with the shared five-family bWAPP suite identified |
| cells | Benign-suite test cells |
| frozen_rule_fp | Cells with a legitimate-task failure under frozen rules |
| stock_or_tuned_fp | Cells with a legitimate-task failure under stock/tuned CRS |
| note | Context only; embedded rule numbers identify public CRS rules, not rule contents |

The tenant_b literal is a synthetic test-tenant label. The TOTAL row is a checksum-like summary, not a thirteenth application. The failed GeoServer A01 suite is excluded from 135 cells / 546 executions; the included GeoServer row is the valid A02 suite. The larger benign task set exposes three PocketBase frozen-rule failures. These failures remain in the data.

## p2_rule_corpus_summary.csv

Three rows: F1 CRS core, F2 official CRS plugins, F3 community rules. repositories, files, and rules are recorded counts. file_count_basis marks the F3 file count as collection_occurrences. Group file counts sum to 172 occurrences while the recorded deduplicated total is 171 unique files; one F3 file was duplicated. S1 checks that arithmetic relationship but does not repeat deduplication.

## p2_rule_frame_summary.csv

Six rows, one for each frame and analysis_unit (directive or chain). binding_count and units are aggregate numerator/denominator; share_pct, wilson_lower_pct, and wilson_upper_pct are percentages rounded to one decimal. The code recomputes their arithmetic using the original Wilson formula. The directive rows describe the original primary aggregate counts; chain rows are sensitivity analysis. They must not be added together. The 119 chain-level units consist of 55 chains and 64 singletons. F2 has 39 chain-level units because one chain contributed two sampled directives. F3's headline range is recorded separately in reported_summary.json. There are no individual labels, annotator names, confidence fields, or response sheets in this table.

## p2_b_boundary_summary.csv

Columns: evaluation, method, correct, total. confirmatory_A01 denotes the four-row PocketBase file evaluation. seven_run_descriptive denotes 40 mutation rows across seven runs and six applications, including development material. Method names identify the recorded v1/v2 feature models and baselines. correct/total are transcribed aggregate prediction counts; the code does not refit a model or independently recover correctness labels. The confirmatory comparison is v2 4/4 versus literal 4/4. The descriptive 40-row table is not a confirmatory superiority result. Post-hoc A02 data are excluded from this minimal package.

## p2_source_layer_summary.csv

Columns: source_category, unit, qualified_units, counterexample, no_counterexample, outcome_scope. Rows cover S1, S2, S3, S6, S7, S8. Units are respectively rule_set, rule_set, rule_set, configuration, case, and application. CE + NoCE equals qualified_units within a row. Adding the rows gives 16 mixed units (6 CE / 10 NoCE), a recorded bookkeeping total, not a statistical sample with interchangeable units. S6's CE is a benign-task failure after a context rename; the other rows refer to attack-side outcomes.

S4 (project rules) and S5 (stock CRS) are represented by the formal summaries, not additional source-layer rows. The S8 table contains only anonymous application-level aggregate counts; no expert-authored rule or blind-review return is included. The source-layer debug duplicate is not included in the 16-unit total. The httpd instrument-ineligible case is not a qualifying S7 case.

## reported_summary.json

Recorded reference values and interpretive boundaries. Formal HTTP-row count, E execution count, corpus unique-file count, source-layer scale and category ladders are transcribed values. They are clearly separated from values recalculated by code. They are not presented as independently verified raw-data results.
