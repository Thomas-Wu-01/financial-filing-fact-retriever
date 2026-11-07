"""Typed declarations for the plugin's tools and task."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Tool(Enum):
    LIST_FILINGS = "list_filings"
    READ_FILING = "read_filing"


class Task(Enum):
    RETRIEVE_FACT = "retrieve-fact"


class FactStatus(Enum):
    FOUND = "found"
    NOT_AVAILABLE = "not_available"


@dataclass
class ListFilingsInput(Output):
    company: Annotated[str, "Exact, case-sensitive company name; an empty string lists every source"]


@dataclass
class FilingMetadata(Output):
    source_id: Annotated[str, "Unique source identifier accepted by read_filing"]
    company: Annotated[str, "Exact fictional company name"]
    filing_type: Annotated[str, "Annual report or quarterly report"]
    period: Annotated[str, "Exact fiscal period identifier"]
    period_basis: Annotated[str, "Whether the fact covers a flow period or a year-end instant"]
    scope: Annotated[str, "Exact consolidated or segment scope"]
    metric: Annotated[str, "Exact metric name"]


@dataclass
class ListFilingsOutput(Output):
    filings: Annotated[list[FilingMetadata], "Matching source metadata in corpus order, without financial values"]


@dataclass
class ReadFilingInput(Output):
    source_id: Annotated[str, "A source identifier returned by list_filings"]


@dataclass
class ReadFilingOutput(Output):
    source_id: Annotated[str, "The requested source identifier"]
    excerpt: Annotated[str, "The complete synthetic filing-style excerpt, including its citation"]


@dataclass
class RetrieveFactInput(Output):
    company: Annotated[str, "Exact, case-sensitive fictional company name"]
    period: Annotated[str, "Exact fiscal period, such as FY2024 or FY2024 Q4"]
    scope: Annotated[str, "Exact scope, such as Consolidated or Segment: Automation"]
    metric: Annotated[str, "Exact metric name: Revenue, Operating income, or Total assets"]


@dataclass
class RetrieveFactOutput(Output):
    status: Annotated[FactStatus, "found when the exact fact exists; otherwise not_available"]
    value: Annotated[str, "Exact decimal string printed in the source, or empty when not_available"]
    unit: Annotated[str, "Exact unit printed in the source, or empty when not_available"]
    source_id: Annotated[str, "Supporting source identifier, or empty when not_available"]


TOOLS = {
    Tool.LIST_FILINGS: (ListFilingsInput, ListFilingsOutput),
    Tool.READ_FILING: (ReadFilingInput, ReadFilingOutput),
}
TASKS = {Task.RETRIEVE_FACT: (RetrieveFactInput, RetrieveFactOutput)}
