import json

from tests.direct.conftest import (
    deploy_watch,
    drift,
    extraction,
    register_mocks,
)


def test_extraction_validator_accepts_semantic_equivalence(
    direct_vm, direct_deploy, direct_alice
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.clear_mocks()
    register_mocks(
        direct_vm,
        extraction("two percent", "The fee will not exceed two percent."),
        comparison="ACCEPT",
    )
    assert direct_vm.run_validator(index=0) is True


def test_extraction_validator_rejects_failed_anchor(
    direct_vm, direct_deploy, direct_alice
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.clear_mocks()
    register_mocks(direct_vm, extraction(anchor="MISMATCH"))
    assert direct_vm.run_validator(index=0) is False


def test_extraction_validator_rejects_semantic_disagreement(
    direct_vm, direct_deploy, direct_alice
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.clear_mocks()
    register_mocks(
        direct_vm,
        extraction("5%", "Maximum withdrawal fee: 5%."),
        comparison="REJECT",
    )
    assert direct_vm.run_validator(index=0) is False


def test_extraction_validator_rejects_malformed_leader_result(
    direct_vm, direct_deploy, direct_alice
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    bad = json.dumps({"clauses": [{"id": "withdrawal_fee"}]})
    assert direct_vm.run_validator(index=0, leader_result=bad) is False


def test_drift_validator_requires_exact_decision_agreement(
    direct_vm, direct_deploy, direct_alice
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.clear_validators()
    direct_vm.clear_mocks()
    direct_vm.warp("2026-01-01T01:00:01Z")
    register_mocks(
        direct_vm,
        extraction("5%", "Maximum withdrawal fee: 5%."),
        drift("MATERIAL"),
    )
    contract.refresh("partner_terms")

    direct_vm.clear_mocks()
    direct_vm.mock_llm(
        r"Classify semantic drift",
        drift("COSMETIC", "Validator considers the wording equivalent."),
    )
    assert direct_vm.run_validator(index=-1) is False


def test_drift_validator_accepts_exact_decision_agreement(
    direct_vm, direct_deploy, direct_alice
):
    contract = deploy_watch(direct_vm, direct_deploy, direct_alice)
    register_mocks(direct_vm, extraction())
    contract.refresh("partner_terms")

    direct_vm.clear_validators()
    direct_vm.clear_mocks()
    direct_vm.warp("2026-01-01T01:00:01Z")
    register_mocks(
        direct_vm,
        extraction("5%", "Maximum withdrawal fee: 5%."),
        drift("MATERIAL"),
    )
    contract.refresh("partner_terms")

    direct_vm.clear_mocks()
    direct_vm.mock_llm(r"Classify semantic drift", drift("MATERIAL"))
    assert direct_vm.run_validator(index=-1) is True
