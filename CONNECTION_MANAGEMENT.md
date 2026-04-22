# 連線超過同時連線數目的解決方案

## 問題分析

您的程式執行時出現"連線超過同時連線數目"的錯誤，主要原因是：

### 1. **Session 未被正確關閉**
- `RedfishClient` 建立的 `requests.Session()` 沒有明確的清理機制
- 如果有多個測試或迴圈建立多個 client 實例，連線會堆積

### 2. **缺少連線池管理**
- 未設定 HTTPAdapter 的連線池限制
- Session 預設會保持多個連線開啟

### 3. **Context Manager 缺失**
- 程式無法使用 `with` 語句自動管理資源
- 容易遺漏 `close()` 呼叫

## 解決方案

### 修改 1: 增強 `RedfishClient` (client.py)

```python
# 新增 imports
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 在 __init__ 中配置連線池
adapter = HTTPAdapter(
    pool_connections=1,  # 最多 1 個持久連線
    pool_maxsize=1,      # 連線池大小為 1
    max_retries=Retry(...)
)
self.session.mount('https://', adapter)
self.session.mount('http://', adapter)

# 新增 Context Manager 支援
def __enter__(self):
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    self.close()
    return False

# 新增析構函數備用清理
def __del__(self):
    try:
        if not self._is_closed:
            self.close()
    except:
        pass
```

### 修改 2: 使用正確的方式建立 Client

#### 方法 A: 使用 Context Manager（推薦）
```python
with RedfishClient("https://192.168.100.60", ("admin", "password")) as client:
    client.login()
    data = client.get_sensor_list()
# 自動關閉連線
```

#### 方法 B: 明確呼叫 close()
```python
client = RedfishClient("https://192.168.100.60", ("admin", "password"))
try:
    client.login()
    data = client.get_sensor_list()
finally:
    client.close()  # 一定要呼叫
```

### 修改 3: 測試框架中的 Fixture 改進

在 `conftest.py` 中使用 session-scoped fixture，確保只建立一個 client：

```python
@pytest.fixture(scope="session")
def bmc_client(target_ip, credentials):
    """建立 BMC 客戶端連線 (session scope)"""
    client = RedfishClient(target_ip, credentials)
    yield client
    # 測試完後自動關閉
    client.close()
```

## 驗證修復

執行測試後，檢查是否有警告或錯誤：

```bash
# 執行簡單測試
python bmc-test-automation/direct_test.py

# 執行 pytest
pytest bmc-test-automation/tests/ -v
```

## 最佳實踐

1. **總是關閉連線** - 使用 `with` 或 `finally` 確保 `close()` 被呼叫
2. **Fixture 為 session scope** - 避免為每個測試建立新的 client
3. **避免全域 client** - 不要在模組層級建立共享的 client
4. **監控連線數** - 使用 `netstat` 或類似工具監控連線狀態

### 檢查開放的連線 (Windows)
```powershell
netstat -ano | findstr "192.168.100.60"
```

### 檢查開放的連線 (Linux)
```bash
netstat -tulpn | grep 192.168.100.60
lsof -i :443
```

## 更新列表

- [x] `client.py`: 增加 HTTPAdapter、Context Manager、析構函數
- [x] `direct_test.py`: 改進 finally 區塊的連線清理
- [x] `conftest.py`: 新增 bmc_client fixture 確保正確的連線管理
