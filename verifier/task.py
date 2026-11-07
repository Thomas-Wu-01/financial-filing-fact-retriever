"""Deterministic grading for retrieve-fact."""

from contract import FactStatus

from .checks import result
from .fixtures import matching_record


def verify_task(arguments, output, reference, workspace):
    if output is None:
        return result(False, "missing task submission")

    record = matching_record(arguments.company, arguments.period, arguments.scope, arguments.metric)
    if record is None:
        if output.status != FactStatus.NOT_AVAILABLE:
            return result(False, "the requested fact is absent; status must be not_available")
        if (output.value, output.unit, output.source_id) != ("", "", ""):
            return result(False, "not_available requires empty value, unit, and source_id")
        return result(True, "the requested fact is not available in the complete corpus")

    if output.status != FactStatus.FOUND:
        return result(False, "the requested fact exists; status must be found")
    if output.value != record["value"]:
        return result(False, "value does not exactly match the authoritative source")
    if output.unit != record["unit"]:
        return result(False, "unit does not exactly match the authoritative source")
    if output.source_id != record["source_id"]:
        return result(False, "source_id does not support the exact company, period, scope, and metric")
    return result(True, "the exact fact and supporting source are correct", source_id=record["source_id"])
