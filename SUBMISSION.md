# Nộp bài cá nhân (hạn theo ca trên LMS)
Tác giả: **Nguyễn Hữu Thịnh**. Bằng chứng kiểm thử: [báo cáo](VERIFICATION_REPORT.md), [log chạy thật](src/reports/validation_m6_m7.txt).
1. Commit mã nguồn, dữ liệu, tài liệu và các report sinh bằng script; không commit môi trường ảo, trace, database và report traps.
2. Mở PR `starter/d09` → `main` trong repo `huuthinh812/K5-L3B-Day9-2A202603726-NguyenHuuThinh-Evaluation-and-Failure-Analysis`.
3. Dán output gate seeded_regression, scorecard, A/A và trap vào PR. Đợi `eval-gate` và `eval-gate-v2` xanh rồi merge vào `main`; giảng viên chấm nhánh `main`.
4. Dán link repo fork lên LMS của ca. Chỉ commit trước hạn theo LMS được tính.

## Core (nên xong trước 17:00)
- [x] `src/lab9/{stats,graders,evalset}.py` đã hoàn thành M1–M4; detection 100%, false alarm 0%
- [x] `src/data/eval/eval_set_v1.jsonl` có `failure_modes`, `labels_v1.json` tách riêng
- [x] `docs/failure_taxonomy.md`, `docs/trace_case.md` (1 case + regression test), `docs/judge_audit.md`, `docs/eval_card.md`, `docs/PRD_v1.1.md`
- [x] `src/reports/baseline_v1.json`, `eval_fixed.json`, `eval_seeded_regression.json` (sinh bằng script)
- [x] `src/harness_map.yaml` có section `eval`
- [x] Job `eval-gate` xanh; output gate exit 1 của `seeded_regression` có trong [PR #1](https://github.com/huuthinh812/K5-L3B-Day9-2A202603726-NguyenHuuThinh-Evaluation-and-Failure-Analysis/pull/1)

## Advanced / Expert (tới 23:59)
- [x] `config/fm_map.yaml`, `config/metric_spec_v2.yaml` (slices, `pass_hat_5`, metric FM-08), `stats.pass_at_k/pass_hat_k`, `gate.slice_check`, `gate.integrity_check`
- [x] `src/data/eval/eval_set_v2.jsonl` + `labels_v2.json` (sinh bằng `evalset --v2 --build`)
- [x] `src/reports/baseline_v2.json` sinh bằng script theo spec 2.2
- [x] Job `eval-gate-v2` trên GitHub chạy và xanh: [CI](https://github.com/huuthinh812/K5-L3B-Day9-2A202603726-NguyenHuuThinh-Evaluation-and-Failure-Analysis/actions/runs/44237958844)
- [x] Mô tả PR có output `lab9.mutation` (scorecard + `--aa`) và 4 dòng `exit 1` của các trap
- [x] `docs/eval_card.md` thêm mục v2: ngưỡng chọn từ A/A, slice nào bắt lỗi nào, và giới hạn cỡ mẫu (bug 1/3 seed không phát hiện ổn định với 5 seed)
