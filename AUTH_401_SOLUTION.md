# 401 未授權錯誤的診斷與解決方案

## 問題說明

您的 BMC 測試出現 **401 未授權 (Unauthorized)** 錯誤，表示：
- ✓ 基本連線成功（HTTP 200）
- ✗ 登入失敗（HTTP 401）
- ✗ 後續請求都被拒絕（HTTP 401）

## 根本原因

### 原始代碼的問題

```python
# ❌ 問題 1: 登入時沒有提供認證
login_resp = session.post(login_url, json=login_data, timeout=10)

# ❌ 問題 2: 登入成功後沒有使用返回的認證信息
if login_resp.status_code == 201:
    # 缺少提取 token 或設定 Authorization header
    pass

# ❌ 問題 3: 後續請求沒有任何認證
sys_resp = session.get(f"{BMC_URL}/redfish/v1/Systems/1", timeout=10)
```

## 解決方案

### 修改 1: 登入時使用 Basic Authentication

GIGABYTE BMC 需要在登入請求時使用 HTTP Basic Authentication：

```python
from requests.auth import HTTPBasicAuth

login_url = f"{BMC_URL}/redfish/v1/SessionService/Sessions"
login_data = {
    "UserName": USERNAME,
    "Password": PASSWORD
}

# ✓ 正確做法: 同時提供 auth 和 JSON body
auth = HTTPBasicAuth(USERNAME, PASSWORD)
login_resp = session.post(login_url, json=login_data, auth=auth, timeout=10)

print(f"登入狀態碼: {login_resp.status_code}")

if login_resp.status_code == 201:
    print("✓ 登入成功")
    # 嘗試提取 token
    try:
        token = login_resp.json().get('token')
        if token:
            session.headers.update({"Authorization": f"Bearer {token}"})
    except:
        pass
```

### 修改 2: 後續請求也使用 Basic Auth

即使在登入後，後續的 GET 請求也需要認證：

```python
# ✓ 方法 A: 使用已設定的 Authorization header
sys_resp = session.get(f"{BMC_URL}/redfish/v1/Systems/1", timeout=10)

# ✓ 方法 B: 直接提供 auth 參數
sys_resp = session.get(
    f"{BMC_URL}/redfish/v1/Systems/1",
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    timeout=10
)
```

## 修復清單

### 已修改的文件

1. **`client.py`**
   - ✓ 登入時添加 `auth=basic_auth` 參數
   - ✓ 提取並使用返回的 token
   - ✓ 後備方案：如果沒有 token，使用 Basic Auth
   - ✓ `_get_with_retry` 中添加 `auth` 參數

2. **`direct_test.py`**
   - ✓ 登入時使用 Basic Auth
   - ✓ 檢查登入響應狀態碼
   - ✓ 顯示登入回應頭和錯誤信息
   - ✓ 改進錯誤處理

3. **`simple_test.py`**
   - ✓ Context manager 中登入時使用 Basic Auth

## 診斷步驟

### 步驟 1: 執行診斷腳本

```bash
python bmc-test-automation/debug_auth.py
```

這個腳本會嘗試多種認證方法並顯示詳細的診斷信息。

### 步驟 2: 檢查輸出

診斷腳本會顯示：
- 基本連線狀態
- 方法 A（Basic Auth）的結果
- 方法 B（無認證）的結果
- 登入響應的詳細信息

### 步驟 3: 基於診斷結果調整

如果診斷腳本顯示特定方法成功，您可以相應地調整代碼。

## 常見的 401 錯誤原因

| 原因 | 症狀 | 解決方案 |
|------|------|--------|
| 沒有使用 Basic Auth | 登入直接返回 401 | 添加 `auth=HTTPBasicAuth(...)` |
| 錯誤的用戶名/密碼 | 登入返回 401 | 驗證 BMC 的實際憑證 |
| 後續請求未認證 | 基本連線成功，其他操作返回 401 | 在所有請求中使用認證 |
| Token 過期 | 初始請求成功，後續請求返回 401 | 在 `_get_with_retry` 中重新登入 |
| Session 未保持 | 登入成功但無法獲取資源 | 確保 `session.cookies` 被保留 |

## 驗證修復

執行以下命令測試修復：

```bash
# 簡單測試
python bmc-test-automation/simple_test.py

# 完整測試
python bmc-test-automation/direct_test.py

# 運行 pytest
cd bmc-test-automation
pytest tests/ -v -s
```

## 如果仍然失敗

### 1. 驗證 BMC 連線狀態

```powershell
# 測試 ICMP ping
ping 192.168.100.60

# 測試 HTTPS 連線
curl -k https://192.168.100.60/redfish/v1/ -u admin:password

# 使用 ipmitool
.\tools\ipmitool\ipmitool.exe -H 192.168.100.60 -U admin -P password chassis status
```

### 2. 檢查 BMC Web 界面

- 訪問 `https://192.168.100.60`（可能需要接受自簽名證書）
- 確認用戶名和密碼正確
- 檢查 BMC 的 Redfish API 是否啟用

### 3. 查看詳細日誌

在代碼中添加日誌級別設定：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

然後查看詳細的請求/響應日誌。

### 4. 聯繫 GIGABYTE 支持

如果上述步驟都無法解決，可以：
- 提供診斷腳本的完整輸出
- 記錄確切的錯誤信息和狀態碼
- 檢查是否有特定版本的 BMC 固件限制
