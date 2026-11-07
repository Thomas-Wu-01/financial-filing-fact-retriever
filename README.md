# Financial Filing Fact Retriever

Financial Filing Fact Retriever is a small `nanoagent.plugin/v0001` challenge for exact evidence retrieval. Its closed corpus contains only fictional companies and generated filing-style excerpts. Every excerpt is synthetic and is **not** a real SEC filing.

The task is deliberately narrow: match one `(company, period, scope, metric)` key, preserve the printed decimal and unit, and cite its source. There is no network access, API key, external collection, manual labeling, unit conversion, rounding, calculation, or restatement.

## Tools

| Tool or task | Contract | Behavior |
|---|---|---|
| `list_filings` | exact company name, or `""` for all | Returns source IDs plus company, filing type, period, period basis, scope, and metric. It never returns financial values or units. |
| `read_filing` | a listed source ID | Returns the complete synthetic excerpt and citation. Unknown IDs fail clearly. |
| `retrieve-fact` | company, period, scope, metric | An `agent` task that may use both tools and must submit a typed status, value, unit, and source ID. |

Matching is exact and case-sensitive. A found response must use `status: found` and copy the source's decimal string, unit, and source ID exactly. A missing response must be exactly:

```json
{"status":"not_available","value":"","unit":"","source_id":""}
```

Example input:

```json
{"company":"Aster Vale Robotics","period":"FY2024","scope":"Consolidated","metric":"Operating income"}
```

Expected output:

```json
{"status":"found","value":"-12.50","unit":"USD million","source_id":"AV24-A-OI"}
```

The 29 fixed records cover three fictional companies and FY2024–FY2025: 17 consolidated annual facts, six quarterly consolidated-revenue distractors, and six annual segment-revenue distractors. Annual `Revenue` and `Operating income` are full-fiscal-year flows. Quarterly revenue is a fiscal-quarter flow with a period such as `FY2024 Q4`. Annual `Total assets` is a stock measured at the fiscal year-end instant even though its lookup period is `FY2024` or `FY2025`. Cinder Peak Energy's FY2025 consolidated operating income is intentionally absent.

## Layout

```text
contract.py             Typed tool and task declarations
nanoagent.yaml          Ready v0001 manifest and agent instructions
src/plugin/             Read-only MCP tool implementations
verifier/fixtures.py    Authoritative fixed synthetic corpus
verifier/               Deterministic semantic tool and task checks
tests/                  Tool, contract, corpus, and verifier tests
product/ and ui/        Catalog metadata, icon, and result renderer
```

The authoritative fixtures are bundled Python constants, so the corpus is reproduced byte-for-byte by the repository and lockfile. Each record has one unique source ID, and each lookup key has at most one record. The tools and verifier use the same bundled fixture module; the verifier never trusts agent-created files or an agent-provided expected answer.

The deterministic verifier checks both tools' inputs and complete outputs. For `retrieve-fact`, it looks up the exact key in the complete fixture corpus. It rejects missing submissions, false unavailability, invented or mismatched citations, wrong statuses, values, units, companies, periods, scopes, and metrics. It compares values as strings, so `0.0`, `-12.50`, and trailing decimal zeros remain significant. Verdicts always contain `valid`, `score`, `message`, and `details`, and NanoAgent reruns verifier calls in its restricted sandbox to detect nondeterminism.

## Develop and run

Use Ubuntu/WSL from this plugin directory:

```bash
uv sync --extra dev --frozen
uv run --frozen pytest
```

Inspect packaging with the existing NanoAgent environment from the NanoAgent project root:

```bash
.venv/bin/nanoagent plugin inspect \
  "/mnt/c/Users/Thomas/Desktop/Rice/Fall 2026/COMP 580/milestone/financial-filing-fact-retriever"
```

Run `retrieve-fact` through RUSH Lab or `nanoagent plugin agent` with a NanoAgent agent-run config, a JSON arguments file matching `RetrieveFactInput`, and no staged input files. Agent execution requires the model credentials configured by that host; tests and inspection require none.

Limitations: this is a small, structured synthetic corpus with exact identifiers. It does not parse real filings, SEC submissions, PDFs, tables, or amended/restated disclosures. It performs no fuzzy matching or financial reasoning. A correct citation proves that the submitted answer matches the corpus, but the final answer alone cannot prove that the agent actually called the evidence tools.
