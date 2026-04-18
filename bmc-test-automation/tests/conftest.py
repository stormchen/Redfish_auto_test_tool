import pytest
import yaml
import os

@pytest.fixture(scope="session")
def target_ip():
    # 依據您的測試目標修改此處
    return "http://192.168.1.100"  # 替換為實際 BMC IP 地址

@pytest.fixture(scope="session")
def credentials():
    # 替換為您使用的帳號密碼或 token
    return ("admin", "password")  # 例如: ("admin", "password")

@pytest.fixture(scope="session")
def thresholds() -> dict:
    # 從 config 載入 thresholds.yaml
    with open(os.path.join(os.path.dirname(__file__), "..", "config", "thresholds.yaml")) as f:
        return yaml.safe_load(f)