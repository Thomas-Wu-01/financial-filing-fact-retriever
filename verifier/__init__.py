"""Deterministic verifier dispatch for tools and the task."""

from contract import Task, Tool

from . import filings, task


def verify_input(tool, value):
    selected = Tool(tool)
    if selected == Tool.LIST_FILINGS:
        return filings.verify_list_input(value)
    return filings.verify_read_input(value)


def verify_output(tool, input_value, output_value, workspace):
    selected = Tool(tool)
    if selected == Tool.LIST_FILINGS:
        return filings.verify_list_output(input_value, output_value, workspace)
    return filings.verify_read_output(input_value, output_value, workspace)


def verify_task(task_id, arguments, output, reference, workspace):
    if Task(task_id) == Task.RETRIEVE_FACT:
        return task.verify_task(arguments, output, reference, workspace)
