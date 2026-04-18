import pytest
import json
import logging

from src.client import RedfishClient
from tests.conftest import target_ip, credentials, thresholds

logger = logging.getLogger(__name__)

def test_normal_sensor_values(client, sensor_name, threshold_config):
    """測試正常門檻值"""
    # 獲取 sensor 資訊
    url = f"/redfish/v1/Chassis/Chassis/1/Sensors/{sensor_name}"
    resp = client.get(url)
    if resp is None:
        pytest.fail(f"Failed to fetch sensor {sensor_name}.")
    data = resp.json()
    value = data.get("Value")
    min_threshold = threshold_config.get("min", 0)
    max_threshold = threshold_config.get("max", float("inf"))
    assert min_threshold <= value <= max_threshold, f"Sensor {sensor_name} value {value} is out of bounds [{min_threshold}, {max_threshold}]"

def test_boundary_conditions(client, sensor_name, threshold_config):
    """測試邊界條件"""
    # 假設測試 min/max 值
    url = f"/redfish/v1/Chassis/Chassis/1/Sensors/{sensor_name}"
    resp = client.get(url)
    if resp is None:
        pytest.fail(f"Failed to fetch sensor {sensor_name}.")
    data = resp.json()
    value = data.get("Value")
    boundary_min = threshold_config.get("boundary_min") or threshold_config.get("min")
    boundary_max = threshold_config.get("boundary_max") or threshold_config.get("max")
    assert value == boundary_min or value == boundary_max, f"Sensor {sensor_name} boundary case failed."

def test_out_of_bounds(client, sensor_name, threshold_config):
    """測試異常值 (超出門檻)"""
    # 假設模擬資料使 sensor 超出範圍
    # 這個測試需更細部模擬，目前為示意
    pass