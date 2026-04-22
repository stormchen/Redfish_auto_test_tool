"""
Pytest 配置與 Fixtures
用於 BMC Redfish 自動化測試
"""
import pytest
import os
import yaml
import logging
import sys
from pathlib import Path

# 導入 RedfishClient
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from client import RedfishClient

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def target_ip():
    """取得目標 BMC IP 地址"""
    ip = os.getenv('BMC_IP', '192.168.100.60')
    logger.info(f"Target BMC IP: {ip}")
    return ip


@pytest.fixture(scope="session")
def credentials():
    """取得認證資訊 (username, password)"""
    username = os.getenv('BMC_USERNAME', 'admin')
    password = os.getenv('BMC_PASSWORD', 'password')
    return (username, password)


@pytest.fixture(scope="session")
def bmc_client(target_ip, credentials):
    """
    建立 BMC Redfish 客戶端連線 (session scope)
    確保整個測試會話只建立一次連線
    """
    logger.info(f"Connecting to BMC at {target_ip}")
    client = RedfishClient(
        base_url=f"https://{target_ip}",
        auth=credentials,
        timeout=10,
        verify_ssl=False
    )
    
    # 嘗試登入
    if client.login():
        logger.info("BMC login successful")
    else:
        logger.warning("BMC login failed, but continuing with basic auth")
    
    yield client
    
    # 測試完後自動關閉連線
    logger.info("Closing BMC connection")
    client.close()


@pytest.fixture(scope="session")
def thresholds_config():
    """
    讀取感應器閾值配置
    """
    config_path = Path(__file__).parent.parent / 'config' / 'thresholds.yaml'
    
    if not config_path.exists():
        raise FileNotFoundError(f"Thresholds config not found at {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Loaded {len(config.get('sensors', {}))} sensor thresholds")
    return config


@pytest.fixture
def sensor_thresholds(thresholds_config):
    """
    取得感應器閾值字典
    """
    return thresholds_config.get('sensors', {})


@pytest.fixture
def boundary_testing_config(thresholds_config):
    """
    取得邊界測試配置
    """
    return thresholds_config.get('boundary_testing', {})


@pytest.fixture
def severity_levels(thresholds_config):
    """
    取得警告等級映射
    """
    return thresholds_config.get('severity_levels', {
        'ok': 0,
        'warning': 1,
        'critical': 2,
        'unknown': 3
    })


class ThresholdValidator:
    """感應器閾值驗證工具"""
    
    @staticmethod
    def validate_reading(sensor_name, reading, threshold):
        """
        驗證感應器讀數是否在閾值內
        
        Returns:
            tuple: (is_valid, status, message)
        """
        if reading is None:
            return True, 'unknown', 'No reading available'
        
        # 檢查是否為數值類型
        try:
            reading_value = float(reading)
        except (ValueError, TypeError):
            return True, 'unknown', f'Invalid reading value: {reading}'
        
        # 檢查 critical 範圍
        critical_min = threshold.get('critical_min')
        critical_max = threshold.get('critical_max')
        if critical_min is not None and reading_value < critical_min:
            return False, 'critical', f'Reading {reading_value} below critical min {critical_min}'
        if critical_max is not None and reading_value > critical_max:
            return False, 'critical', f'Reading {reading_value} above critical max {critical_max}'
        
        # 檢查 warning 範圍
        warning_min = threshold.get('warning_min')
        warning_max = threshold.get('warning_max')
        if warning_min is not None and reading_value < warning_min:
            return True, 'warning', f'Reading {reading_value} below warning min {warning_min}'
        if warning_max is not None and reading_value > warning_max:
            return True, 'warning', f'Reading {reading_value} above warning max {warning_max}'
        
        # 檢查 normal 範圍
        normal_min = threshold.get('min')
        normal_max = threshold.get('max')
        if normal_min is not None and reading_value < normal_min:
            return False, 'critical', f'Reading {reading_value} below normal min {normal_min}'
        if normal_max is not None and reading_value > normal_max:
            return False, 'critical', f'Reading {reading_value} above normal max {normal_max}'
        
        return True, 'ok', f'Reading {reading_value} within acceptable range'


@pytest.fixture
def threshold_validator():
    """提供閾值驗證工具"""
    return ThresholdValidator()


def pytest_configure(config):
    """
    Pytest 初始化鉤子
    """
    # 確保報告目錄存在
    Path('reports/html').mkdir(parents=True, exist_ok=True)
    Path('reports/logs').mkdir(parents=True, exist_ok=True)
    logger.info("Test environment configured")


def pytest_collection_modifyitems(config, items):
    """
    修改測試項目，添加自訂標記
    """
    for item in items:
        # 為所有測試添加 'bmc' 標記
        if 'bmc' not in [mark.name for mark in item.iter_markers()]:
            item.add_marker(pytest.mark.bmc)


@pytest.fixture(autouse=True)
def log_test_start_end(request):
    """
    自動為每個測試記錄開始和結束日誌
    """
    logger.info(f"{'='*60}")
    logger.info(f"Starting: {request.node.name}")
    logger.info(f"{'='*60}")
    
    yield
    
    logger.info(f"Completed: {request.node.name}")
    logger.info(f"{'='*60}\n")

