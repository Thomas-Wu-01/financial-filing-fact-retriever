from __future__ import annotations

from dataclasses import fields

import pytest

from contract import ListFilingsInput, ReadFilingInput
from plugin.filings import list_filings, read_filing


def test_lists_all_value_free_metadata_in_fixed_order() -> None:
    output = list_filings(ListFilingsInput(company=""))
    assert len(output.filings) == 29
    assert [filing.source_id for filing in output.filings[:3]] == ["AV24-A-REV", "AV24-A-OI", "AV24-A-ASSET"]
    assert {field.name for field in fields(output.filings[0])} == {
        "source_id",
        "company",
        "filing_type",
        "period",
        "period_basis",
        "scope",
        "metric",
    }


def test_filters_by_exact_company_name() -> None:
    output = list_filings(ListFilingsInput(company="Cinder Peak Energy"))
    assert len(output.filings) == 9
    assert all(filing.company == "Cinder Peak Energy" for filing in output.filings)
    with pytest.raises(ValueError, match="exact company name"):
        list_filings(ListFilingsInput(company="cinder peak energy"))


def test_reads_complete_synthetic_excerpt_and_rejects_unknown_source() -> None:
    output = read_filing(ReadFilingInput(source_id="AV24-A-OI"))
    assert output.source_id == "AV24-A-OI"
    assert output.excerpt == (
        "SYNTHETIC FILING EXCERPT — not a real SEC filing.\n"
        "Source ID: AV24-A-OI\n"
        "Company: Aster Vale Robotics\n"
        "Filing: Annual report\n"
        "Period: FY2024 (full fiscal year)\n"
        "Scope: Consolidated\n"
        "Metric: Operating income\n"
        "Reported fact: Operating income was -12.50 USD million.\n"
        "Citation: AV24-A-OI"
    )
    with pytest.raises(ValueError, match="unknown source_id: INVENTED"):
        read_filing(ReadFilingInput(source_id="INVENTED"))
