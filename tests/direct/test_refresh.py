from tests.direct.conftest import (
    URL,
    clauses_json,
    deploy_watch,
    drift,
    extraction,
    register_mocks,
)


def test_baseline_refresh_stores_normalized_facts(direct_vm, direct_deploy, direct_alice):
    direct_vm.check_pickling = True
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())

    contract.refresh("partner_terms")

    clause = contract.latest("partner_terms", "withdrawal_fee")
    assert clause["value"] == "2%"
    assert clause["evidence_quote"] == "Maximum withdrawal fee: 2%."
    assert clause["confidence"] == 96
    assert clause["last_drift"] == "BASELINE"
    assert clause["last_snapshot"] == 1

    snapshot = contract.get_snapshot("partner_terms", 1)
    assert snapshot["snapshot"] == 1
    assert snapshot["counts"] == {"material": 0, "cosmetic": 0, "unchanged": 0}
    assert len(snapshot["clauses"]) == 2


def test_material_drift_updates_indexes(direct_vm, direct_deploy, direct_alice):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.clear_mocks()
    direct_vm.warp("2026-01-01T01:00:01Z")
    register_mocks(
        direct_vm,
        extraction("5%", "Maximum withdrawal fee: 5%."),
        drift("MATERIAL"),
    )
    contract.refresh("partner_terms")

    clause = contract.get_clause("partner_terms", "withdrawal_fee")
    assert clause["value"] == "5%"
    assert clause["last_drift"] == "MATERIAL"
    assert clause["last_change_snapshot"] == 2
    assert clause["last_material_snapshot"] == 2

    status = contract.changed_since("partner_terms", "withdrawal_fee", 1)
    assert status["changed"] is True
    assert status["materially_changed"] is True
    assert status["latest_snapshot"] == 2

    subscription = contract.get_subscription("partner_terms")
    assert subscription["material_count"] == 1
    assert subscription["unchanged_count"] == 1


def test_cosmetic_drift_is_not_material(direct_vm, direct_deploy, direct_alice):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.clear_mocks()
    direct_vm.warp("2026-01-01T01:00:01Z")
    register_mocks(
        direct_vm,
        extraction("two percent", "We charge no more than two percent."),
        drift("COSMETIC", "Equivalent fee expressed in words."),
    )
    contract.refresh("partner_terms")

    status = contract.changed_since("partner_terms", "withdrawal_fee", 1)
    assert status["changed"] is True
    assert status["materially_changed"] is False
    assert contract.get_subscription("partner_terms")["cosmetic_count"] == 1


def test_public_refresh_is_rate_limited(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("refresh interval has not elapsed"):
        contract.refresh("partner_terms")


def test_refresh_interval_is_shared_by_url(direct_vm, direct_deploy, direct_alice):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    contract.watch("same_url_second_watch", URL, clauses_json(), 3600)
    with direct_vm.expect_revert("refresh interval has not elapsed"):
        contract.refresh("same_url_second_watch")


def test_inactive_subscription_cannot_refresh(direct_vm, direct_deploy, direct_alice):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    contract.set_active("partner_terms", False)
    with direct_vm.expect_revert("subscription is inactive"):
        contract.refresh("partner_terms")
