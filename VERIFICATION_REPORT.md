# Báo cáo kiểm thử ngày 18/11/2026

Tác giả/eval owner: **Nguyễn Hữu Thịnh**. Cập nhật sau hoàn thiện: toàn bộ pytest hiện có **37 tests pass** (thêm 4 test cho grader đề xuất). Lệnh `python -m lab9.verify` lưu kiểm tra exit code và output thực tế vào `src/reports/validation_m6_m7.txt`.

Lần xác minh cuối: **16/16 kiểm tra đạt**, bao gồm điều kiện mọi delta A/A bằng 0; mutation 3/3, false alarm 0, cả 4 traps bị chặn.

Nhánh kiểm thử: `starter/d09` (working tree dựa trên commit `17c3dcf`). Python 3.13.18, môi trường `.verification/venv`.

## Kết quả đã chạy

- `lab9.smoke`: `M0 PASS`.
- Toàn bộ pytest sau khi bổ sung regression tests: **37 passed**, không deselect (`-o addopts= -p no:cacheprovider`).
- `lab9.evalset --check` (v1 `8cb82c5e0c4e`) và `lab9.evalset --v2` (v2 `af6cd54b0d77`): **0 problem(s)**.
- Tone judge: `P=0.857`, `R=0.8`, `kappa=0.757`, `PASS floors`.
- Helpful judge: `P=1.0`, `R=0.3`, `kappa=0.375`, `FAIL floors` (đúng yêu cầu loại khỏi gate).
- M3 `lab9.mutation --detect`: **detection 100.00%** (target >=80%), **false alarms 0.00%** (target <=10%) sau khi bổ sung `ProposalAmountCorrect` (`proposal_amount_correct` trong `metric_spec.yaml` và `metric_spec_v2.yaml`).
- `lab9.ci_check` trên v1 (`swarm` chạy lại vs `reports/baseline_v1.json`): `exit 0 — baseline and spec look sound`.
- Gate v1:
  - `eval_fixed.json` vs `baseline_v1.json`: `exit 0 — merge`.
  - `eval_seeded_regression.json` vs `baseline_v1.json`: `exit 1 — blocked: refund_amount_correct, reply_amount_matches_ledger, pass_rate` (pass_rate Δ -0.271, CI [-0.500, -0.057]).
- Baseline v2 tự so sánh (`baseline_v2.json` vs `baseline_v2.json`): `exit 0 — merge` (mọi delta và CI bằng 0).
- Mutation v2 (`lab9.mutation --spec config/metric_spec_v2.yaml --baseline reports/baseline_v2.json`): **mutation score 3/3 · false alarms 0** (`fixed` và `honest_refactor` merge; `seeded_regression`, `slice_regression`, `flaky_regression` bị block).
- A/A với bộ seed `66,77,88,99,110`: tất cả metric có delta `+0.0000`, `pass_hat_5=0.8929` ở cả hai bộ seed.
- Bốn traps công khai (`lab9.traps`): đều bị chặn với `exit 1 — blocked: integrity` (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec`); lệnh `lab9.traps` trả `exit 0`.

## Việc còn lại trước khi nộp

Ghi nhận môi trường: một lần A/A có pass_rate Δ=0.0072, pass_hat_5 Δ=0.0358; chẩn đoán lại hai bộ seed đạt cùng pass_rate=0.9786, pass_hat_5=0.8929. Verifier đã bổ sung điều kiện mọi delta A/A phải bằng 0 để không chỉ dựa vào exit code. Chưa xác định nguyên nhân dao động đơn lẻ này.

1. Commit và push toàn bộ thay đổi hiện tại trên `starter/d09` lên remote (đặc biệt các file vừa cập nhật ở working tree và `VERIFICATION_REPORT.md` nếu muốn giữ liên kết từ `docs/eval_card.md`).
2. Kiểm tra lại `git remote -v` và git author nếu cần đồng bộ tài khoản GitHub của Nguyễn Hữu Thịnh.
3. Mở PR từ `starter/d09` → `main`, điền checklist `SUBMISSION.md`, dán output `seeded_regression`, `lab9.mutation` (scorecard + `--aa`) và 4 dòng trap vào mô tả PR, rồi kiểm tra job GitHub Actions (`eval-gate` và `eval-gate-v2`) chạy xanh.
