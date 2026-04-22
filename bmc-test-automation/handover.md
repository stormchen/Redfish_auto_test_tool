# Handover — Phase 1 未完成項目與後續步驟

簡易狀態：Phase 1 的主要修正已完成（client token/logout、感測器詳單、pytest 測試與 thresholds.yaml）。以下為尚未完成或需驗證的項目，以及具體執行指令。

剩下的工作清單
- 更新 `requirements.txt`：固定並驗證所有套件版本，確保 CI/本地環境一致。
- 執行完整 pytest：在 `bmc-test-automation` 目錄執行全套測試，確認無失敗。
- 在 `pytest.ini` 註冊 `bmc` mark：移除 UnknownMark 警告。
- 儲存原始 HTTP 回應：使用 `client.save_response()` 或等效方式將原始 JSON 存到 `reports/raw/`，以供審核。
- 處理 TLS 警告：評估是否啟用憑證驗證或有選擇地抑制 InsecureRequestWarning。
- 最終閾值微調：根據完整測試結果調整 `config/thresholds.yaml`。
- 變更提交與 PR：將修改 commit 並建立 Pull Request，請同儕審查。

關鍵檔案位置
- 測試與程式： bmc-test-automation/
- 閾值設定： bmc-test-automation/config/thresholds.yaml
- 測試檔案： bmc-test-automation/tests/
- 報表輸出： bmc-test-automation/reports/html/report.html
- 原始回應建議儲放： bmc-test-automation/reports/raw/

如何執行（建議步驟）

1) 建議於虛擬環境中操作

```bash
cd "bmc-test-automation"
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2) 執行完整 pytest（含 HTML 報告）

```bash
cd "bmc-test-automation"
python -m pytest -v --html=reports/html/report.html
```

3) 在 `pytest.ini` 中加入 marker（消除警告）

在 `pytest.ini` 的 `[pytest]` 區段下加入：

```
markers =
    bmc: mark tests requiring BMC connection
```

4) 儲存原始 HTTP 回應（建議實作）

在 `src/client.py` 或測試流程中，呼叫：

```python
# 範例：
client.save_response(resp, 'reports/raw/sensor-<name>.json')
```

5) 處理 TLS 警告

- 若能取得 BMC 的有效憑證：設定 `verify` 為憑證路徑。
- 若無法在短期內取得憑證，可在測試前抑制警告（短期折衷）：

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

（長期建議：不要抑制，改為安裝/指定憑證）

6) 閾值微調流程

- 依測試結果檢視 `reports/html/threshold_validation_results.json` 與 HTML 報表。
- 若出現非預期的 Critical/Warning，調整 `config/thresholds.yaml` 相對感測器條目後重跑測試。

7) 提交與 PR

```bash
git add .
git commit -m "phase1: thresholds, tests, client fixes, reports"
git push origin <branch>
# 建立 PR 並請同仁 review
```

重要備註
- 已確認 `direct_test.py` 能成功登入並執行 logout（DELETE session）。
- 已確認 `tests/test_sensor_thresholds.py::test_sensor_threshold_validation` 個別測試可通過；仍需執行全套測試以最終驗證。
- 報表與原始輸出位置： `reports/html/report.html`, `reports/html/sensor_report.txt`, `reports/html/threshold_validation_results.json`。

如需我代為執行的項目（選一或多項）：
- 代為更新並鎖定 `requirements.txt` 版本
- 執行完整 pytest 並回報結果
- 在 `pytest.ini` 中加入 marker 並 commit
- 新增自動儲存 raw responses 的小修改

指定要我先做哪一項，或直接回覆「全部」，我就開始執行。
