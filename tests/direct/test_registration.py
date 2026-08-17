import json

from tests.direct.conftest import CONTRACT, URL, clauses_json, deploy_watch


def test_registers_versioned_subscription(direct_vm, direct_deploy, direct_alice):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)

    subscription = contract.get_subscription("partner_terms")
    assert subscription["url"] == URL
    assert subscription["active"] is True
    assert subscription["latest_snapshot"] == 0
    assert subscription["min_refresh_seconds"] == 3600

    clause = contract.get_clause("partner_terms", "withdrawal_fee")
    assert clause["initialized"] is False
    assert clause["is_anchor"] is False

    anchor = contract.get_clause("partner_terms", "document_title")
    assert anchor["is_anchor"] is True
    assert anchor["anchor_expected"] == "Example Partner Terms"


def test_rejects_subscription_without_anchor(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT, sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    no_anchor = json.dumps(
        [{"id": "fee", "question": "What is the maximum withdrawal fee?"}]
    )
    with direct_vm.expect_revert("provide 1..3 anchor clauses"):
        contract.watch("terms", URL, no_anchor, 3600)


def test_rejects_duplicate_clause_id(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT, sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    duplicate = json.dumps(
        [
            {
                "id": "title",
                "question": "What is the document title?",
                "anchor_expected": "Terms",
            },
            {"id": "title", "question": "What title appears here?"},
        ]
    )
    with direct_vm.expect_revert("duplicate clause id"):
        contract.watch("terms", URL, duplicate, 3600)


def test_only_owner_can_pause(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only subscription owner"):
        contract.set_active("partner_terms", False)

    direct_vm.sender = direct_alice
    contract.set_active("partner_terms", False)
    assert contract.get_subscription("partner_terms")["active"] is False


def test_rejects_bad_refresh_interval(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy(CONTRACT, sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("min_refresh_seconds must be 300..2592000"):
        contract.watch("terms", URL, clauses_json(), 10)
