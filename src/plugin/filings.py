"""Read-only access to the authoritative bundled synthetic corpus."""

from __future__ import annotations

from contract import (
    FilingMetadata,
    ListFilingsInput,
    ListFilingsOutput,
    ReadFilingInput,
    ReadFilingOutput,
)
from verifier.fixtures import COMPANIES, RECORDS, excerpt, record_by_source


def _metadata(record: dict[str, str]) -> FilingMetadata:
    return FilingMetadata(
        source_id=record["source_id"],
        company=record["company"],
        filing_type=record["filing_type"],
        period=record["period"],
        period_basis=record["period_basis"],
        scope=record["scope"],
        metric=record["metric"],
    )


def list_filings(given: ListFilingsInput) -> ListFilingsOutput:
    if given.company and given.company not in COMPANIES:
        raise ValueError("company must be empty or an exact company name in the synthetic corpus")
    records = RECORDS if not given.company else tuple(record for record in RECORDS if record["company"] == given.company)
    return ListFilingsOutput(filings=[_metadata(record) for record in records])


def read_filing(given: ReadFilingInput) -> ReadFilingOutput:
    record = record_by_source(given.source_id)
    if record is None:
        raise ValueError(f"unknown source_id: {given.source_id}")
    return ReadFilingOutput(source_id=given.source_id, excerpt=excerpt(record))
