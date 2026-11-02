# Reproduction coverage

Run code/main.py --verify-only first, then code/main.py. Every command is offline. A successful run reports PASS and the number of aggregate checks. Any failed integrity, schema, or arithmetic check exits nonzero. The default output directory is outputs/; --output can select a directory outside the release. Output paths inside the sealed input tree are rejected except under outputs/.

| Result | What S1 actually verifies |
|---|---|
| Formal 19/12/155/18 | Counts runs, explicitly maps samples into application clusters, sums cells, and counts effect-family strings |
| Endpoint 19/19 | Counts runs containing the exact CE token; does not count contexts as independent runs |
| Payload 16/16 | Requires source qualification and the exact NoCE outcome; absent payload arms remain absent |
| Stock qualification 5/19 | Counts qualification flags, preserving ineligible arms |
| E 12/135/3/6 | Recomputes application totals and FP-cell totals; retains PocketBase failures |
| Rule counts 47 repositories / 6,892 rules | Sums the three source-group aggregates; unique-file count is a recorded reference |
| Rule-frame intervals | Recalculates shares and Wilson bounds from aggregate counts; does not reconstruct labels |
| B 4/4 versus 4/4 | Checks the reported count comparison and preserves the unmet superiority criterion; does not train a model |
| Source layer 16 / 6 / 10 | Checks the decomposition of six source-category summaries; this is mixed-unit bookkeeping |

The expected values in data/reported_summary.json come from the same recorded study results. Agreement is a consistency check against those results, not an independent reproduction of the original measurements.

Outputs are deterministic and contain no generation timestamp: six TABLE_p2_*.md files, summary.json, and verification.json. summary.json separates recalculated values from transcribed reference values. verification.json records the individual aggregate checks and inventory result.

Unavailable in S1: raw effect observations, reconstruction of benign executions or HTTP-row counts, corpus acquisition/deduplication, annotation agreement or bootstrap estimates, original rule parsing, B fitting/predictions, and online deployment-change execution. No new experiments were performed, no original results were changed, and no population protection rate is estimated.

The release was also checked after ZIP extraction and from a working directory different from the release directory. Local review evidence is delivered separately from the public upload tree.
