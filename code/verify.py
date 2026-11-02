"""Summary-only checks adapted from P2 verify.py; no private label inputs."""
import json
from utils import load_csv, wilson


SCHEMAS = {
    "p2_formal_runs_19.csv": ["run", "sample", "cells", "endpoint_source_qualified", "payload_source_qualified", "stock_source_qualified", "endpoint_outcomes", "payload_outcomes", "stock_outcomes", "vulnerability_family"],
    "p2_benign_suite_12apps.csv": ["application", "cells", "frozen_rule_fp", "stock_or_tuned_fp", "note"],
    "p2_rule_corpus_summary.csv": ["frame", "repositories", "files", "file_count_basis", "rules"],
    "p2_rule_frame_summary.csv": ["frame", "analysis_unit", "binding_count", "units", "share_pct", "wilson_lower_pct", "wilson_upper_pct"],
    "p2_b_boundary_summary.csv": ["evaluation", "method", "correct", "total"],
    "p2_source_layer_summary.csv": ["source_category", "unit", "qualified_units", "counterexample", "no_counterexample", "outcome_scope"],
}
CLUSTERS = {
    "apprise": "Apprise", "bwapp_lfi": "bWAPP", "bwapp_redirect": "bWAPP",
    "bwapp_sqli": "bWAPP", "bwapp_traversal": "bWAPP", "bwapp_xpath": "bWAPP",
    "consul": "Consul", "geoserver": "GeoServer", "minio": "MinIO", "minio_response": "MinIO",
    "mutillidae": "Mutillidae", "nodered": "Node-RED", "nodered_adminread": "Node-RED",
    "opensearch": "OpenSearch", "pocketbase": "PocketBase", "pocketbase_file": "PocketBase",
    "shiro": "Shiro", "solr": "Solr", "zeppelin": "Zeppelin",
}
CE = "COUNTEREXAMPLE"
NO_CE = "NO_COUNTEREXAMPLE_IN_EXECUTED_CASE"
INELIGIBLE = "SOURCE_INELIGIBLE_OR_TARGET_NOT_INSTANTIATED"


def run(root):
    data = root / "data"
    reference = json.loads((data / "reported_summary.json").read_text(encoding="utf-8"))
    if reference.get("schema_version") != 1:
        raise ValueError("Unexpected reference schema")
    datasets = {name: load_csv(data / name, fields) for name, fields in SCHEMAS.items()}
    checks = []
    def check(name, actual, expected):
        ok = actual == expected
        checks.append({"check": name, "actual": actual, "expected": expected, "passed": ok})
        if not ok:
            raise ValueError("Check failed: " + name + " (" + str(actual) + " != " + str(expected) + ")")
    def integer(value):
        number = int(value)
        if number < 0 or str(number) != value:
            raise ValueError("Expected nonnegative integer")
        return number

    runs = datasets["p2_formal_runs_19.csv"]
    check("formal unique run IDs", len({r["run"] for r in runs}), len(runs))
    check("formal sample set", sorted(r["sample"] for r in runs), sorted(CLUSTERS))
    for row in runs:
        integer(row["cells"])
        for arm in ["endpoint", "payload", "stock"]:
            q = row[arm + "_source_qualified"]
            check(row["sample"] + ": valid " + arm + " qualification", q in {"true", "false", "none"}, True)
            outcomes = row[arm + "_outcomes"].split(";") if row[arm + "_outcomes"] else []
            check(row["sample"] + ": valid " + arm + " outcomes", all(x in {CE, NO_CE, INELIGIBLE} for x in outcomes), True)
            if q == "true":
                check(row["sample"] + ": qualified " + arm + " has evaluated outcome", bool(outcomes) and INELIGIBLE not in outcomes, True)
            elif q == "none":
                check(row["sample"] + ": absent " + arm + " is empty", outcomes, [])
            else:
                check(row["sample"] + ": unqualified " + arm + " is not target success", outcomes, [INELIGIBLE])
    formal = {
        "runs": len(runs), "application_clusters": len({CLUSTERS[r["sample"]] for r in runs}),
        "cells": sum(integer(r["cells"]) for r in runs),
        "effect_families": len({r["vulnerability_family"] for r in runs}),
        "endpoint_counterexample_runs": sum(CE in r["endpoint_outcomes"].split(";") for r in runs),
        "payload_qualified_runs": sum(r["payload_source_qualified"] == "true" for r in runs),
        "payload_no_counterexample_runs": sum(r["payload_outcomes"] == NO_CE and r["payload_source_qualified"] == "true" for r in runs),
        "stock_qualified_runs": sum(r["stock_source_qualified"] == "true" for r in runs),
    }
    for key, value in formal.items():
        check("formal " + key, value, reference["formal"][key])
    geo = next(r for r in runs if r["sample"] == "geoserver")
    check("GeoServer mixed endpoint outcomes retained", geo["endpoint_outcomes"], CE + ";" + NO_CE)

    benign_rows = datasets["p2_benign_suite_12apps.csv"]
    totals = [r for r in benign_rows if r["application"] == "TOTAL"]
    check("one benign TOTAL row", len(totals), 1)
    body = [r for r in benign_rows if r["application"] != "TOTAL"]
    check("benign unique applications", len({r["application"] for r in body}), len(body))
    check("benign application alignment", sorted(r["application"].split(" (")[0] for r in body), sorted(set(CLUSTERS.values())))
    benign = {"applications": len(body)}
    for column, key in [("cells", "cells"), ("frozen_rule_fp", "frozen_fp_cells"), ("stock_or_tuned_fp", "stock_or_tuned_fp_cells")]:
        benign[key] = sum(integer(r[column]) for r in body)
        check("benign TOTAL " + column, benign[key], integer(totals[0][column]))
    for row in body:
        check(row["application"] + ": FP cell bounds", max(integer(row["frozen_rule_fp"]), integer(row["stock_or_tuned_fp"])) <= integer(row["cells"]), True)
    for key, value in benign.items():
        check("benign " + key, value, reference["benign"][key])
    check("frozen benign failures retained", [r["application"] for r in body if integer(r["frozen_rule_fp"])], ["PocketBase"])

    corpus_rows = datasets["p2_rule_corpus_summary.csv"]
    check("corpus frame coverage", sorted(r["frame"] for r in corpus_rows), ["F1", "F2", "F3"])
    corpus = {key: sum(integer(r[key]) for r in corpus_rows) for key in ["repositories", "rules"]}
    for key, value in corpus.items():
        check("corpus " + key, value, reference["corpus"][key])
    check("F3 occurrence-count basis", next(r["file_count_basis"] for r in corpus_rows if r["frame"] == "F3"), "collection_occurrences")
    check("corpus one documented duplicate file", sum(integer(r["files"]) for r in corpus_rows) - reference["corpus"]["unique_files"], 1)

    frame_rows = datasets["p2_rule_frame_summary.csv"]
    check("frame unit coverage", sorted((r["frame"], r["analysis_unit"]) for r in frame_rows), sorted((f, u) for f in ["F1", "F2", "F3"] for u in ["directive", "chain"]))
    frame_results = []
    for row in frame_rows:
        k, n = integer(row["binding_count"]), integer(row["units"])
        check(row["frame"] + " " + row["analysis_unit"] + ": count bounds", 0 <= k <= n and n > 0, True)
        share = round(100 * k / n, 1)
        lo, hi = wilson(k, n)
        label = row["frame"] + " " + row["analysis_unit"]
        for key, value in [("share_pct", share), ("wilson_lower_pct", lo), ("wilson_upper_pct", hi)]:
            check(label + " " + key, value, float(row[key]))
        frame_results.append({"frame": row["frame"], "analysis_unit": row["analysis_unit"], "binding_count": k, "units": n, "share_pct": share, "wilson_lower_pct": lo, "wilson_upper_pct": hi})
    f3 = {r["analysis_unit"]: r for r in frame_results if r["frame"] == "F3"}
    check("F3 directive-to-chain difference in percentage points", round(f3["chain"]["share_pct"] - f3["directive"]["share_pct"], 1), 27.5)
    check("F3 reported range retained", reference["frame_headline"]["F3"].startswith("19-30/40"), True)

    b_rows = datasets["p2_b_boundary_summary.csv"]
    check("B unique evaluation/method pairs", len({(r["evaluation"], r["method"]) for r in b_rows}), len(b_rows))
    required = {(e, m) for e, methods in [("confirmatory_A01", ["v2_model", "v1_model", "literal", "exact_anchor", "class_endpoint", "object_key"]), ("seven_run_descriptive", ["v2_model", "v1_model", "literal", "exact_anchor", "class_endpoint", "source_replay"])] for m in methods}
    check("B evaluation/method coverage", sorted((r["evaluation"], r["method"]) for r in b_rows), sorted(required))
    for row in b_rows:
        check("B " + row["evaluation"] + " " + row["method"] + ": count bounds", 0 <= integer(row["correct"]) <= integer(row["total"]), True)
        check("B denominator " + row["evaluation"], integer(row["total"]), 4 if row["evaluation"] == "confirmatory_A01" else 40)
    confirm = {r["method"]: integer(r["correct"]) for r in b_rows if r["evaluation"] == "confirmatory_A01"}
    check("B confirmatory model", confirm["v2_model"], reference["b"]["confirmatory_v2_correct"])
    check("B confirmatory literal", confirm["literal"], reference["b"]["confirmatory_literal_correct"])
    check("B superiority criterion remains unmet", confirm["v2_model"] > confirm["literal"], reference["b"]["superiority_criterion_met"])

    source_rows = datasets["p2_source_layer_summary.csv"]
    check("source-layer category coverage", sorted(r["source_category"] for r in source_rows), ["S1", "S2", "S3", "S6", "S7", "S8"])
    for row in source_rows:
        check(row["source_category"] + ": outcome decomposition", integer(row["counterexample"]) + integer(row["no_counterexample"]), integer(row["qualified_units"]))
        check(row["source_category"] + ": mixed-unit semantics", (row["unit"], row["outcome_scope"]), ("configuration", "benign_task_failure") if row["source_category"] == "S6" else ({"S1": "rule_set", "S2": "rule_set", "S3": "rule_set", "S7": "case", "S8": "application"}[row["source_category"]], "attack"))
    source = {"qualified_mixed_units": sum(integer(r["qualified_units"]) for r in source_rows), "counterexamples_mixed_units": sum(integer(r["counterexample"]) for r in source_rows), "no_counterexamples_mixed_units": sum(integer(r["no_counterexample"]) for r in source_rows)}
    for key, value in source.items():
        check("source-layer " + key, value, reference["source_layer"][key])
    summary = {"schema_version": 1, "version": "1.0.0", "scope": "S1 summary-only", "recomputed": {"formal": formal, "benign": benign, "corpus": corpus, "frames": frame_results, "b_superiority_criterion_met": confirm["v2_model"] > confirm["literal"], "source_layer_mixed_unit_arithmetic": source}, "transcribed_reference": reference, "checks_passed": len(checks)}
    return datasets, summary, checks
