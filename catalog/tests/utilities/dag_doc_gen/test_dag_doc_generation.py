from typing import NamedTuple
from unittest import mock

import pytest

from catalog.tests.dags.providers.provider_api_scripts.resources.provider_data_ingester.mock_provider_data_ingester import (
    MockProviderDataIngester,
)
from catalog.utilities.dag_doc_gen import dag_doc_generation
from catalog.utilities.dag_doc_gen.dag_doc_generation import DagInfo
from providers.provider_workflows import ProviderWorkflow


class DagMock(NamedTuple):
    # schedule_interval used here because the Dag model does not actually have a
    # schedule attribute
    schedule_interval: str | None
    doc_md: str | None
    catchup: bool
    tags: list[str]


DAG_ID = "sample_dag_123"
SAMPLE_MEDIA_TYPES = ("m1", "m2")
PROVIDER_WORKFLOW_INSTANCE = mock.MagicMock()
PROVIDER_WORKFLOW_INSTANCE.media_types = SAMPLE_MEDIA_TYPES
_MODULE = "catalog.utilities.dag_doc_gen.dag_doc_generation"


@pytest.mark.parametrize("schedule", ["@daily", None])
@pytest.mark.parametrize(
    "doc, expected_doc",
    [
        (None, None),
        ("Sample simple doc", "Sample simple doc"),
        ("# Big header", "### Big header"),
    ],
)
@pytest.mark.parametrize(
    "tags, type_",
    [
        (None, "other"),
        ([], "other"),
        (["foo"], "foo"),
        (["foo", "bar"], "foo"),
    ],
)
@pytest.mark.parametrize(
    "provider_workflow, catchup, expected_dated",
    [
        # Dated is always equal to provider_workflow.dated
        (
            ProviderWorkflow(ingester_class=MockProviderDataIngester, dated=False),
            True,
            False,
        ),
        (
            ProviderWorkflow(ingester_class=MockProviderDataIngester, dated=False),
            False,
            False,
        ),
        (
            ProviderWorkflow(ingester_class=MockProviderDataIngester, dated=True),
            True,
            True,
        ),
        (
            ProviderWorkflow(ingester_class=MockProviderDataIngester, dated=True),
            False,
            True,
        ),
        # If ProviderWorkflow is None, fall back to the value of 'catchup'
        (None, True, True),
        (None, False, False),
    ],
)
def test_get_dags_info(
    schedule, doc, expected_doc, tags, type_, provider_workflow, catchup, expected_dated
):
    dag = DagMock(schedule_interval=schedule, doc_md=doc, catchup=catchup, tags=tags)
    expected = DagInfo(
        dag_id=DAG_ID,
        schedule=schedule,
        doc=expected_doc,
        dated=expected_dated,
        type_=type_,
        provider_workflow=provider_workflow,
    )
    with mock.patch(f"{_MODULE}.get_provider_workflows") as provider_workflow_mock:
        provider_workflow_mock.return_value.get.return_value = provider_workflow
        actual = dag_doc_generation.get_dags_info({DAG_ID: dag})[0]
        assert actual == expected


@pytest.mark.parametrize(
    "dag_info, is_provider, expected",
    [
        # Most info missing
        (
            DagInfo(
                dag_id=DAG_ID,
                schedule=None,
                doc=None,
                type_="",
                dated=False,
                provider_workflow=None,
            ),
            False,
            """
## Special Name

| DAG ID | Schedule Interval |
| --- | --- |
| `sample_dag_123` | `None` |
""",
        ),
        # Most info present
        (
            DagInfo(
                dag_id=DAG_ID,
                schedule="@daily",
                doc="A doc does exist here",
                type_="",
                dated=False,
                provider_workflow=None,
            ),
            False,
            """
## Special Name

| DAG ID | Schedule Interval |
| --- | --- |
| [`sample_dag_123`](#sample_dag_123) | `@daily` |
""",
        ),
        # Provider workflow with most
        (
            DagInfo(
                dag_id=DAG_ID,
                schedule="@daily",
                doc="A doc does exist here",
                type_="",
                dated=False,
                provider_workflow=PROVIDER_WORKFLOW_INSTANCE,
            ),
            True,
            """
## Special Name

| DAG ID | Schedule Interval | Dated | Media Type(s) |
| --- | --- | --- | --- |
| [`sample_dag_123`](#sample_dag_123) | `@daily` | `False` | m1, m2 |
""",
        ),
    ],
)
def test_generate_type_subsection(dag_info, is_provider, expected):
    actual = dag_doc_generation.generate_type_subsection(
        "Special Name", [dag_info], is_provider
    )
    assert actual.strip() == expected.strip()


def test_generate_dag_doc():
    expected = (
        dag_doc_generation.PREAMBLE
        + """\
 1. [T1](#t1)

## T1

| DAG ID | Schedule Interval |
| --- | --- |
| `a` | `None` |
| [`b`](#b) | `None` |

"""
        + dag_doc_generation.MIDAMBLE
        + """\
 1. [`b`](#b)


## `b`

this one has a doc
"""
    )
    with (mock.patch(f"{_MODULE}.get_dags_info") as get_dags_info_mock,):
        # Return in reverse order to ensure they show up in the correct order
        get_dags_info_mock.return_value = [
            DagInfo("b", None, "this one has a doc", "t1", False, None),
            DagInfo("a", None, None, "t1", False, None),
        ]
        actual = dag_doc_generation.generate_dag_doc()
        assert actual == expected
