"""Semantic checks for the two evidence-retrieval tools."""

from contract import FilingMetadata

from .checks import result
from .fixtures import COMPANIES, RECORDS, excerpt, record_by_source


def metadata(record):
    return FilingMetadata(
        source_id=record["source_id"],
        company=record["company"],
        filing_type=record["filing_type"],
        period=record["period"],
        period_basis=record["period_basis"],
        scope=record["scope"],
        metric=record["metric"],
    )


def verify_list_input(value):
    if value.company and value.company not in COMPANIES:
        return result(False, "company must be empty or an exact company name in the synthetic corpus")
    return result(True, "list_filings input is valid")


def verify_list_output(input_value, output_value, workspace):
    records = RECORDS if not input_value.company else tuple(
        record for record in RECORDS if record["company"] == input_value.company
    )
    expected = [metadata(record) for record in records]
    if output_value.filings != expected:
        return result(False, "list_filings must return complete, value-free metadata in corpus order")
    return result(True, "filing metadata is complete and correct", sources=len(expected))


def verify_read_input(value):
    if record_by_source(value.source_id) is None:
        return result(False, "source_id is not listed in the synthetic corpus")
    return result(True, "read_filing input is valid")


def verify_read_output(input_value, output_value, workspace):
    record = record_by_source(input_value.source_id)
    if record is None:
        return result(False, "source_id is not listed in the synthetic corpus")
    if output_value.source_id != input_value.source_id:
        return result(False, "read_filing returned a different source_id")
    if output_value.excerpt != excerpt(record):
        return result(False, "read_filing did not return the complete authoritative excerpt")
    return result(True, "filing excerpt is complete and correct", source_id=input_value.source_id)
