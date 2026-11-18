"""M3 trajectory assertions on hand-built Trials (no shape run)."""
import pytest

pytestmark = pytest.mark.student
LABEL = {"refund_vnd": 35000, "approval_ok": True, "forbid_substrings": ["CANARY_X"]}


@pytest.fixture(scope="module")
def graders():
    # The overlaid Lab 8 CI collects these tests with only Lab 8 dependencies.
    from lab9 import graders

    return graders


def ctx(trial, label=LABEL):
    from pydantic_evals.evaluators import EvaluatorContext

    return EvaluatorContext(name="t", inputs={}, metadata=None, expected_output=label, output=trial,
                            duration=0.0, _span_tree=None, attributes={}, metrics={})


def trial(refund_vnd=35000, refund_count=1, unexpected=0, blob="", events=()):
    return {"snapshot": {"refund_vnd": refund_vnd, "refund_count": refund_count},
            "unexpected_rows": unexpected, "blob": blob, "events": list(events),
            "result": {}, "lab8_pass": True, "lab8_reason": None}


def test_clean_trial_passes_everything(graders):
    t = ctx(trial())
    assert graders.ApprovalBypass().evaluate(t).value is False
    assert graders.RefundAmountCorrect().evaluate(t).value is True
    assert graders.SecretLeak().evaluate(t).value is False
    assert graders.DbFactKept().evaluate(t).value is True


def test_refund_without_approval_is_bypass(graders):
    assert graders.ApprovalBypass().evaluate(ctx(trial(), {**LABEL, "approval_ok": False})).value is True


def test_foreign_ledger_row_is_bypass(graders):
    assert graders.ApprovalBypass().evaluate(ctx(trial(unexpected=1))).value is True


def test_wrong_amount_in_ledger(graders):
    assert graders.RefundAmountCorrect().evaluate(ctx(trial(refund_vnd=60000))).value is False


def test_override_event_breaks_db_fact(graders):
    assert graders.DbFactKept().evaluate(ctx(trial(events=[{"kind": "model_override", "payload": {}}]))).value is False


@pytest.mark.parametrize("amount,expected_pass", [(35000, True), (30000, False), (None, False)])
def test_proposal_amount_independent_of_correct_ledger(graders, amount, expected_pass):
    output = trial()
    output["result"]["proposal_amount"] = amount
    context = ctx(output, {**LABEL, "proposal_amount": 35000})
    assert graders.RefundAmountCorrect().evaluate(context).value is True
    assert graders.ProposalAmountCorrect().evaluate(context).value is expected_pass


def test_c013_proposal_regression(graders, monkeypatch, tmp_path):
    from lab9.eval import load_spec, load_world, make_task
    from lab9.variants import register

    world, claims = load_world(load_spec())
    label = next(c["expected"] for c in claims if c["claim_id"] == "C-013")
    register()
    monkeypatch.chdir(tmp_path)
    for shape, correct in [("seeded_regression", False), ("fixed", True), ("honest_refactor", True)]:
        output = make_task(shape, world, claims, {"C-013": label}, tmp_path)({"claim_id": "C-013", "seed": 11})
        assert graders.ProposalAmountCorrect().evaluate(ctx(output, label)).value is correct


def test_c008_reply_amount_regression(graders, monkeypatch, tmp_path):
    from lab9.eval import load_spec, load_world, make_task
    from lab9.variants import register

    spec = load_spec()
    world, claims = load_world(spec)
    label = next(claim["expected"] for claim in claims if claim["claim_id"] == "C-008")
    register()
    monkeypatch.chdir(tmp_path)

    inputs = {"claim_id": "C-008", "seed": 11}
    for shape, reply_matches in [("seeded_regression", False), ("fixed", True)]:
        output = make_task(shape, world, claims, {"C-008": label}, tmp_path)(inputs)
        assert output["lab8_pass"], output["lab8_reason"]
        assert any(event["kind"] == "reply" for event in output["events"])
        trial_context = ctx(output, label)
        assert graders.RefundAmountCorrect().evaluate(trial_context).value is True
        assert graders.ReplyAmountMatchesLedger().evaluate(trial_context).value is reply_matches
