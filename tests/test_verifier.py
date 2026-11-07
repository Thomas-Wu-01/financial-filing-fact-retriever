from __future__ import annotations

import pytest
from slimconfig import build_output

import verifier
from contract import (
    FactStatus,
    ListFilingsInput,
    ListFilingsOutput,
    ReadFilingInput,
    ReadFilingOutput,
    RetrieveFactInput,
    RetrieveFactOutput,
)
from plugin.filings import list_filings, read_filing
from verifier.fixtures import RECORDS

ANNUAL_REVENUE = RetrieveFactInput(
    company="Aster Vale Robotics",
    period="FY2024",
    scope="Consolidated",
    metric="Revenue",
)
ANNUAL_REVENUE_ANSWER = RetrieveFactOutput(
    status=FactStatus.FOUND,
    value="1250.40",
    unit="USD million",
    source_id="AV24-A-REV",
)


def verify(arguments: RetrieveFactInput, output: RetrieveFactOutput | None):
    return verifier.verify_task("retrieve-fact", arguments, output, None, ".")


def test_accepts_correct_exact_retrieval() -> None:
    verdict = verify(ANNUAL_REVENUE, ANNUAL_REVENUE_ANSWER)
    assert verdict == {
        "valid": True,
        "score": 1.0,
        "message": "the exact fact and supporting source are correct",
        "details": {"source_id": "AV24-A-REV"},
    }


@pytest.mark.parametrize(
    "changed",
    [
        {"value": "1250.4"},
        {"unit": "USD thousand"},
        {"source_id": "INVENTED"},
        {"status": FactStatus.NOT_AVAILABLE, "value": "", "unit": "", "source_id": ""},
    ],
)
def test_rejects_wrong_value_unit_source_or_status(changed: dict[str, object]) -> None:
    values = {
        "status": ANNUAL_REVENUE_ANSWER.status,
        "value": ANNUAL_REVENUE_ANSWER.value,
        "unit": ANNUAL_REVENUE_ANSWER.unit,
        "source_id": ANNUAL_REVENUE_ANSWER.source_id,
    }
    values.update(changed)
    assert verify(ANNUAL_REVENUE, RetrieveFactOutput(**values))["valid"] is False


@pytest.mark.parametrize(
    "source_id",
    [
        "BH24-A-REV",
        "AV25-A-REV",
        "AV24-Q4-REV",
        "AV24-S-AUTO",
        "AV24-A-OI",
    ],
)
def test_rejects_citations_for_wrong_company_period_quarter_scope_or_metric(source_id: str) -> None:
    output = RetrieveFactOutput(
        status=FactStatus.FOUND,
        value="1250.40",
        unit="USD million",
        source_id=source_id,
    )
    assert verify(ANNUAL_REVENUE, output)["valid"] is False


def test_accepts_absent_fact_and_rejects_false_unavailability() -> None:
    absent = RetrieveFactInput(
        company="Cinder Peak Energy",
        period="FY2025",
        scope="Consolidated",
        metric="Operating income",
    )
    unavailable = RetrieveFactOutput(status=FactStatus.NOT_AVAILABLE, value="", unit="", source_id="")
    assert verify(absent, unavailable)["valid"] is True
    nonempty = RetrieveFactOutput(status=FactStatus.NOT_AVAILABLE, value="0", unit="", source_id="")
    assert verify(absent, nonempty)["valid"] is False
    assert verify(ANNUAL_REVENUE, unavailable)["valid"] is False


def test_rejects_missing_submission() -> None:
    verdict = verify(ANNUAL_REVENUE, None)
    assert verdict["valid"] is False
    assert verdict["message"] == "missing task submission"


def test_zero_negative_and_decimal_formatting_are_exact() -> None:
    negative = RetrieveFactInput("Aster Vale Robotics", "FY2024", "Consolidated", "Operating income")
    zero = RetrieveFactInput("Aster Vale Robotics", "FY2025", "Consolidated", "Operating income")
    assert verify(negative, RetrieveFactOutput(FactStatus.FOUND, "-12.50", "USD million", "AV24-A-OI"))["valid"] is True
    assert verify(zero, RetrieveFactOutput(FactStatus.FOUND, "0.0", "USD million", "AV25-A-OI"))["valid"] is True
    assert verify(negative, RetrieveFactOutput(FactStatus.FOUND, "-12.5", "USD million", "AV24-A-OI"))["valid"] is False
    assert verify(zero, RetrieveFactOutput(FactStatus.FOUND, "0", "USD million", "AV25-A-OI"))["valid"] is False


def test_malformed_task_output_is_rejected_at_contract_boundary() -> None:
    with pytest.raises(ValueError, match="missing field.*source_id"):
        build_output({"status": "found", "value": "1", "unit": "USD million"}, RetrieveFactOutput)
    with pytest.raises(ValueError, match="not a valid FactStatus"):
        build_output({"status": "maybe", "value": "1", "unit": "USD million", "source_id": "x"}, RetrieveFactOutput)


def test_tool_verifier_accepts_complete_outputs_and_rejects_changes() -> None:
    list_input = ListFilingsInput(company="Blue Harbor Foods")
    listed = list_filings(list_input)
    assert verifier.verify_input("list_filings", list_input)["valid"] is True
    assert verifier.verify_input("list_filings", ListFilingsInput(company="blue harbor foods"))["valid"] is False
    assert verifier.verify_output("list_filings", list_input, listed, ".")["valid"] is True
    incomplete = ListFilingsOutput(filings=listed.filings[:-1])
    assert verifier.verify_output("list_filings", list_input, incomplete, ".")["valid"] is False

    read_input = ReadFilingInput(source_id="CP24-A-REV")
    read = read_filing(read_input)
    assert verifier.verify_input("read_filing", read_input)["valid"] is True
    assert verifier.verify_output("read_filing", read_input, read, ".")["valid"] is True
    changed = ReadFilingOutput(source_id=read.source_id, excerpt=read.excerpt + " altered")
    assert verifier.verify_output("read_filing", read_input, changed, ".")["valid"] is False
    wrong_source = ReadFilingOutput(source_id="CP24-A-OI", excerpt=read.excerpt)
    assert verifier.verify_output("read_filing", read_input, wrong_source, ".")["valid"] is False
    assert verifier.verify_input("read_filing", ReadFilingInput(source_id="UNKNOWN"))["valid"] is False


def test_fixture_ids_and_lookup_keys_are_unique() -> None:
    source_ids = [record["source_id"] for record in RECORDS]
    keys = [(record["company"], record["period"], record["scope"], record["metric"]) for record in RECORDS]
    assert len(RECORDS) == 29
    assert len(source_ids) == len(set(source_ids))
    assert len(keys) == len(set(keys))


def test_verdicts_are_deterministic() -> None:
    assert verify(ANNUAL_REVENUE, ANNUAL_REVENUE_ANSWER) == verify(ANNUAL_REVENUE, ANNUAL_REVENUE_ANSWER)
