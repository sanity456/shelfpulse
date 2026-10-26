import json
import re


URL_1 = "https://example.com/stock/period-1.json"
URL_2 = "https://example.com/stock/period-2.json"
DESCRIPTION = "Reusable stainless steel kettle, model K20, 1.5 liter capacity."
PROMPT = "Decide whether this fetched stock snapshot describes the same product"


def body(period, quantity, description=DESCRIPTION):
    return json.dumps({"item_description": description, "period": period, "quantity": quantity})


def observation(shelf, direct_vm, item, oid, url, period, quantity, verdict="MATCH", description=DESCRIPTION):
    direct_vm.mock_web(re.escape(url), {"status": 200, "body": body(period, quantity, description)})
    direct_vm.mock_llm(rf".*{re.escape(PROMPT)}.*", json.dumps({"match": verdict}))
    return shelf.record_observation(item, oid, url)


def register(shelf, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    return shelf.register_item("K20", DESCRIPTION, 3, 12)


def test_requires_two_fresh_consecutive_low_snapshots_for_one_order(shelf, direct_vm, direct_alice):
    register(shelf, direct_vm, direct_alice)
    observation(shelf, direct_vm, "K20", "period-1", URL_1, 1, 3)
    state = shelf.get_item(direct_alice, "K20")
    assert state["status"] == "MONITORING"
    assert state["recommended_order"] == 0
    observation(shelf, direct_vm, "K20", "period-2", URL_2, 2, 2)
    state = shelf.get_item(direct_alice, "K20")
    assert state["status"] == "RESTOCK_DUE"
    assert state["low_streak"] == 2
    assert state["recommended_order"] == 10


def test_non_low_snapshot_resets_consecutive_confirmation(shelf, direct_vm, direct_alice):
    register(shelf, direct_vm, direct_alice)
    observation(shelf, direct_vm, "K20", "p1", URL_1, 1, 2)
    observation(shelf, direct_vm, "K20", "p2", URL_2, 2, 4)
    assert shelf.get_item(direct_alice, "K20")["low_streak"] == 0
    assert shelf.get_item(direct_alice, "K20")["status"] == "MONITORING"


def test_rejects_repeated_period_and_observation_id(shelf, direct_vm, direct_alice):
    register(shelf, direct_vm, direct_alice)
    observation(shelf, direct_vm, "K20", "p1", URL_1, 1, 2)
    direct_vm.mock_web(re.escape(URL_1), {"status": 200, "body": body(1, 2)})
    direct_vm.mock_llm(rf".*{re.escape(PROMPT)}.*", json.dumps({"match": "MATCH"}))
    with direct_vm.expect_revert("evidence_period_not_consecutive"):
        shelf.record_observation("K20", "p2", URL_1)
    with direct_vm.expect_revert("observation_id_reused"):
        shelf.record_observation("K20", "p1", URL_2)


def test_only_item_owner_can_submit_observation(shelf, direct_vm, direct_alice, direct_bob):
    register(shelf, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("item_missing"):
        shelf.record_observation("K20", "p1", URL_1)


def test_mismatch_or_unclear_evidence_fails_closed(shelf, direct_vm, direct_alice):
    register(shelf, direct_vm, direct_alice)
    direct_vm.mock_web(re.escape(URL_1), {"status": 200, "body": body(1, 1, "A different ceramic coffee mug model.")})
    direct_vm.mock_llm(rf".*{re.escape(PROMPT)}.*", json.dumps({"match": "MISMATCH"}))
    with direct_vm.expect_revert("evidence_item_not_confirmed"):
        shelf.record_observation("K20", "p1", URL_1)
    assert shelf.get_item(direct_alice, "K20")["observation_count"] == 0


def test_external_evidence_failures_do_not_change_state(shelf, direct_vm, direct_alice):
    register(shelf, direct_vm, direct_alice)
    cases = [
        ("https://example.com/missing", {"status": 404, "body": "missing"}, "evidence_http_404"),
        ("https://example.com/empty", {"status": 200, "body": ""}, "evidence_empty"),
        ("https://example.com/oversized", {"status": 200, "body": "x" * 24_001}, "evidence_too_large"),
        ("https://example.com/not-utf8", {"status": 200, "body": b"\xff"}, "evidence_not_utf8"),
    ]
    for index, (url, response, error) in enumerate(cases):
        direct_vm.mock_web(re.escape(url), response)
        with direct_vm.expect_revert(error):
            shelf.record_observation("K20", f"bad-{index}", url)
    state = shelf.get_item(direct_alice, "K20")
    assert state["observation_count"] == 0
    assert state["status"] == "MONITORING"


def test_validator_rejects_forged_leader_fields(shelf, direct_vm, direct_alice):
    register(shelf, direct_vm, direct_alice)
    direct_vm.mock_web(re.escape(URL_1), {"status": 200, "body": body(1, 2)})
    direct_vm.mock_llm(rf".*{re.escape(PROMPT)}.*", json.dumps({"match": "MATCH"}))
    shelf.record_observation("K20", "p1", URL_1)
    assert direct_vm.run_validator() is True
    forged = {"period": 1, "quantity": 999, "match": "MATCH", "evidence_hash": "sha256:forged", "source_url": URL_1}
    assert direct_vm.run_validator(leader_result=forged) is False


def test_invalid_snapshot_period_and_bad_model_shape_fail_closed(shelf, direct_vm, direct_alice):
    register(shelf, direct_vm, direct_alice)
    direct_vm.mock_web(re.escape(URL_1), {"status": 200, "body": body(3, 2)})
    with direct_vm.expect_revert("evidence_period_not_consecutive"):
        shelf.record_observation("K20", "p1", URL_1)
    assert shelf.get_item(direct_alice, "K20")["observation_count"] == 0
