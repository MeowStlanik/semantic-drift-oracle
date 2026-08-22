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


def test_same_url_subscriptions_enforce_their_own_cadence(
    direct_vm, direct_deploy, direct_alice
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    contract.watch("fast_watch", URL, clauses_json(), 300)
    register_mocks(direct_vm, extraction(), drift("UNCHANGED"))

    # Baseline the 3600-second subscription first.
    contract.refresh("partner_terms")

    # A faster subscription for the same URL refreshes twice in the meantime.
    direct_vm.warp("2026-01-01T00:05:01Z")
    contract.refresh("fast_watch")
    direct_vm.warp("2026-01-01T00:10:02Z")
    contract.refresh("fast_watch")

    # The fast subscription is still limited by its own 300-second cadence.
    with direct_vm.expect_revert("refresh interval has not elapsed"):
        contract.refresh("fast_watch")

    # The fast watch must not postpone the 3600-second watch. Under the old
    # global url_last_refresh logic this call was blocked until 01:10:02.
    direct_vm.warp("2026-01-01T01:00:01Z")
    contract.refresh("partner_terms")

    assert contract.get_subscription("fast_watch")["latest_snapshot"] == 2
    assert contract.get_subscription("partner_terms")["latest_snapshot"] == 2


def test_inactive_subscription_cannot_refresh(direct_vm, direct_deploy, direct_alice):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    contract.set_active("partner_terms", False)
    with direct_vm.expect_revert("subscription is inactive"):
        contract.refresh("partner_terms")
