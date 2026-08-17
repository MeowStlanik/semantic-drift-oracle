"""Network smoke test. Run explicitly with: gltest tests/integration -v -s."""

import json

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


@pytest.mark.integration
def test_deploy_register_and_read(default_account):
    factory = get_contract_factory("SemanticDriftOracle")
    contract = factory.deploy()

    clauses = json.dumps(
        [
            {
                "id": "fee",
                "question": "What is the maximum withdrawal fee?",
                "anchor_expected": "",
            },
            {
                "id": "title",
                "question": "What is the document title?",
                "anchor_expected": "Example Terms",
            },
        ]
    )
    tx = contract.watch(
        args=["integration_terms", "https://example.com/terms", clauses, 3600]
    ).transact()
    assert tx_execution_succeeded(tx)

    subscription = contract.get_subscription(args=["integration_terms"]).call()
    assert subscription["id"] == "integration_terms"
    assert subscription["latest_snapshot"] == 0
