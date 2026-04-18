# BMC Redfish Automation Test Framework

此專案用來自動化測試 BMC 的 Redfish API 行為，並驗證感測器門檻值。

## 功能
- 支援 sensor 門檻驗證
- 支援邊界測試
- 自動產生 HTML/PDF 報告

## 安裝方式
```bash
pip install -r requirements.txt
```

## 執行方式
```bash
pytest
```

## 自訂參數
可編輯 `config/thresholds.yaml` 定義要測試的感測器與對應門檻。

## 貢獻
歡迎所有貢獻與改善。