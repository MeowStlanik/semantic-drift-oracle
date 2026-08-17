import json


CONTRACT = "contracts/semantic_drift_oracle.py"
URL = "https://example.com/terms"


def clauses_json():
    return json.dumps(
        [
            {
                "id": "withdrawal_fee",
                "question": "What is the maximum withdrawal fee?",
                "anchor_expected": "",
            },
            {
                "id": "document_title",
                "question": "What is the title of this document?",
                "anchor_expected": "Example Partner Terms",
            },
        ]
    )


def extraction(fee="2%", fee_quote="Maximum withdrawal fee: 2%.", anchor="MATCH"):
    return json.dumps(
        {
            "clauses": [
                {
                    "id": "withdrawal_fee",
                    "value": fee,
                    "evidence_quote": fee_quote,
                    "confidence": 96,
                    "anchor_status": "NOT_ANCHOR",
                },
                {
                    "id": "document_title",
                    "value": "Example Partner Terms",
                    "evidence_quote": "Example Partner Terms",
                    "confidence": 99,
                    "anchor_status": anchor,
                },
            ]
        }
    )


def drift(kind="MATERIAL", rationale="The maximum fee changed."):
    return json.dumps(
        {
            "clauses": [
                {
                    "id": "withdrawal_fee",
                    "drift": kind,
                    "rationale": rationale,
                },
                {
                    "id": "document_title",
                    "drift": "UNCHANGED",
                    "rationale": "The title is unchanged.",
                },
            ]
        }
    )


def register_mocks(vm, extraction_response, drift_response=None, comparison="ACCEPT"):
    vm.mock_web(
        r"example\.com/terms",
        {
            "status": 200,
            "body": "Example Partner Terms. Maximum withdrawal fee: 2%.",
        },
    )
    vm.mock_llm(r"document fact extractor", extraction_response)
    vm.mock_llm(r"CONSENSUS SEMANTIC COMPARISON", comparison)
    if drift_response is not None:
        vm.mock_llm(r"Classify semantic drift", drift_response)


def deploy_watch(vm, direct_deploy, owner):
    vm.warp("2026-01-01T00:00:00Z")
    contract = direct_deploy(CONTRACT, sdk_version="v0.2.12")
    vm.sender = owner
    contract.watch("partner_terms", URL, clauses_json(), 3600)
    return contract
