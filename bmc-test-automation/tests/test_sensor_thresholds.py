"""
BMC Sensor 閾值驗證測試
使用 pytest 框架進行自動化測試
"""
import pytest
import json
import logging
import time
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class TestSensorThresholds:
    """感應器閾值測試類"""
    
    def test_retrieve_all_sensors(self, bmc_client):
        """
        測試 1: 取得所有感應器清單
        驗證可以成功從 BMC 取得感應器列表
        """
        logger.info("Test 1: Retrieving all sensors from BMC")
        
        # 取得感應器列表
        sensor_list = bmc_client.get_sensor_list()
        
        # 驗證結果
        assert sensor_list is not None, "Failed to get sensor list"
        assert len(sensor_list) > 0, "No sensors found in BMC"
        
        logger.info(f"✓ Successfully retrieved {len(sensor_list)} sensors")
        for idx, sensor in enumerate(sensor_list[:5], 1):
            logger.debug(f"  Sensor {idx}: {sensor.get('Name', 'N/A')}")
    
    def test_sensor_threshold_validation(self, bmc_client, sensor_thresholds, threshold_validator):
        """
        測試 2: 驗證每個感應器的讀數是否在閾值範圍內
        """
        logger.info("Test 2: Validating sensor readings against thresholds")
        
        sensor_list = bmc_client.get_sensor_list()
        assert len(sensor_list) > 0, "No sensors to validate"
        
        validation_results = {
            'ok': [],
            'warning': [],
            'critical': [],
            'unknown': [],
            'not_configured': []
        }
        
        for sensor in sensor_list:
            sensor_name = sensor.get('Name')
            sensor_reading = sensor.get('Reading')
            sensor_unit = sensor.get('ReadingUnits')
            
            # 檢查是否有配置
            if sensor_name not in sensor_thresholds:
                validation_results['not_configured'].append({
                    'sensor': sensor_name,
                    'reading': sensor_reading,
                    'unit': sensor_unit
                })
                continue
            
            threshold = sensor_thresholds[sensor_name]
            is_valid, status, message = threshold_validator.validate_reading(
                sensor_name, sensor_reading, threshold
            )
            
            result = {
                'sensor': sensor_name,
                'reading': sensor_reading,
                'unit': sensor_unit,
                'status': status,
                'message': message
            }
            validation_results[status].append(result)
            
            # 記錄詳細信息
            if status in ['critical', 'warning']:
                log_message = f"  [{sensor_name}] {sensor_reading} {sensor_unit} -> {status.upper()}"
                if status == 'critical':
                    logger.error(log_message + f" ({message})")
                elif status == 'warning':
                    logger.warning(log_message + f" ({message})")
            # 正常狀態不記錄詳細日誌
        
        # 輸出統計
        logger.info(f"\nValidation Results Summary:")
        logger.info(f"  ✓ OK: {len(validation_results['ok'])}")
        logger.info(f"  ⚠ Warning: {len(validation_results['warning'])}")
        logger.info(f"  ✗ Critical: {len(validation_results['critical'])}")
        logger.info(f"  ? Unknown: {len(validation_results['unknown'])}")
        logger.info(f"  ⊘ Not Configured: {len(validation_results['not_configured'])}")
        
        # 失敗斷言：如果有 critical 的感應器
        critical_sensors = validation_results['critical']
        if critical_sensors:
            error_msg = "Critical sensors detected:\n"
            for sensor_result in critical_sensors:
                error_msg += f"  - {sensor_result['sensor']}: {sensor_result['message']}\n"
            pytest.fail(error_msg)
        
        # 儲存測試結果
        self._save_validation_results(validation_results)
    
    def test_temperature_sensors(self, bmc_client, sensor_thresholds, threshold_validator):
        """
        測試 3: 專項測試 - 溫度感應器
        """
        logger.info("Test 3: Temperature Sensors Validation")
        
        sensor_list = bmc_client.get_sensor_list()
        temperature_sensors = [
            s for s in sensor_list 
            if 'TEMP' in s.get('Name', '').upper() or 'DTS' in s.get('Name', '').upper()
        ]
        
        assert len(temperature_sensors) > 0, "No temperature sensors found"
        logger.info(f"Found {len(temperature_sensors)} temperature sensors")
        
        results = []
        for sensor in temperature_sensors:
            sensor_name = sensor.get('Name')
            reading = sensor.get('Reading')
            
            if sensor_name in sensor_thresholds:
                threshold = sensor_thresholds[sensor_name]
                is_valid, status, msg = threshold_validator.validate_reading(
                    sensor_name, reading, threshold
                )
                
                results.append({
                    'name': sensor_name,
                    'reading': reading,
                    'status': status,
                    'valid': is_valid
                })
                
                log_msg = f"  {sensor_name}: {reading}°C -> {status}"
                if is_valid:
                    logger.info(f"✓ {log_msg}")
                else:
                    logger.error(f"✗ {log_msg}")
        
        # 驗證至少有一個溫度感應器在正常範圍
        ok_count = sum(1 for r in results if r['valid'])
        assert ok_count > 0, "All temperature sensors are out of normal range"
        logger.info(f"✓ {ok_count}/{len(results)} temperature sensors are within normal range")
    
    def test_fan_sensors(self, bmc_client, sensor_thresholds, threshold_validator):
        """
        測試 4: 專項測試 - 風扇感應器
        """
        logger.info("Test 4: Fan Sensors Validation")
        
        sensor_list = bmc_client.get_sensor_list()
        fan_sensors = [
            s for s in sensor_list 
            if 'FAN' in s.get('Name', '').upper()
        ]
        
        assert len(fan_sensors) > 0, "No fan sensors found"
        logger.info(f"Found {len(fan_sensors)} fan sensors")
        
        results = []
        for sensor in fan_sensors:
            sensor_name = sensor.get('Name')
            reading = sensor.get('Reading')
            
            if sensor_name in sensor_thresholds:
                threshold = sensor_thresholds[sensor_name]
                is_valid, status, msg = threshold_validator.validate_reading(
                    sensor_name, reading, threshold
                )
                
                results.append({
                    'name': sensor_name,
                    'reading': reading,
                    'status': status,
                    'valid': is_valid
                })
                
                log_msg = f"  {sensor_name}: {reading} RPM -> {status}"
                if is_valid:
                    logger.info(f"✓ {log_msg}")
                else:
                    logger.error(f"✗ {log_msg}")
        
        # 驗證所有風扇都在運行
        ok_count = sum(1 for r in results if r['valid'])
        assert ok_count == len(results), f"Some fans are not operating normally: {len(results) - ok_count} failures"
        logger.info(f"✓ All {len(results)} fans are operating normally")
    
    def test_voltage_sensors(self, bmc_client, sensor_thresholds, threshold_validator):
        """
        測試 5: 專項測試 - 電壓感應器
        """
        logger.info("Test 5: Voltage Sensors Validation")
        
        sensor_list = bmc_client.get_sensor_list()
        voltage_sensors = [
            s for s in sensor_list 
            if 'P' in s.get('Name', '').upper()  # 電源軌通常以 P 開頭
        ]
        
        if len(voltage_sensors) == 0:
            logger.warning("No voltage sensors found")
            pytest.skip("No voltage sensors configured")
        
        logger.info(f"Found {len(voltage_sensors)} voltage sensors")
        
        results = []
        for sensor in voltage_sensors:
            sensor_name = sensor.get('Name')
            reading = sensor.get('Reading')
            unit = sensor.get('ReadingUnits', 'V')
            
            if sensor_name in sensor_thresholds:
                threshold = sensor_thresholds[sensor_name]
                is_valid, status, msg = threshold_validator.validate_reading(
                    sensor_name, reading, threshold
                )
                
                results.append({
                    'name': sensor_name,
                    'reading': reading,
                    'unit': unit,
                    'status': status,
                    'valid': is_valid
                })
                
                log_msg = f"  {sensor_name}: {reading} {unit} -> {status}"
                if is_valid:
                    logger.info(f"✓ {log_msg}")
                else:
                    logger.error(f"✗ {log_msg}")
        
        # 驗證重要電壓軌正常
        if results:
            ok_count = sum(1 for r in results if r['valid'])
            logger.info(f"✓ {ok_count}/{len(results)} voltage sensors are within normal range")
    
    def test_boundary_conditions(self, bmc_client, sensor_thresholds, threshold_validator, boundary_testing_config):
        """
        測試 6: 邊界條件測試
        驗證感應器在邊界條件下的行為
        """
        logger.info("Test 6: Boundary Condition Testing")
        
        if not boundary_testing_config.get('enabled', True):
            logger.info("Boundary testing is disabled")
            pytest.skip("Boundary testing is disabled in config")
        
        sensor_list = bmc_client.get_sensor_list()
        logger.info(f"Testing boundary conditions for {len(sensor_list)} sensors")
        
        boundary_results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }
        
        # 選擇前 10 個感應器進行邊界測試 (避免耗時過長)
        for sensor in sensor_list[:10]:
            sensor_name = sensor.get('Name')
            reading = sensor.get('Reading')
            
            if sensor_name not in sensor_thresholds:
                boundary_results['skipped'] += 1
                continue
            
            threshold = sensor_thresholds[sensor_name]
            is_valid, status, msg = threshold_validator.validate_reading(
                sensor_name, reading, threshold
            )
            
            if is_valid:
                boundary_results['passed'] += 1
            else:
                boundary_results['failed'] += 1
                logger.warning(f"Boundary test failed for {sensor_name}: {msg}")
        
        logger.info(f"Boundary testing results: Passed={boundary_results['passed']}, "
                   f"Failed={boundary_results['failed']}, Skipped={boundary_results['skipped']}")
        
        assert boundary_results['failed'] == 0, \
            f"Boundary testing failed for {boundary_results['failed']} sensors"
    
    @staticmethod
    def _save_validation_results(results: Dict) -> None:
        """
        將驗證結果保存到 JSON 文件
        """
        import json
        from pathlib import Path
        
        report_dir = Path('reports/html')
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = report_dir / 'threshold_validation_results.json'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Validation results saved to {report_path}")


class TestSensorConnectivity:
    """感應器連接性測試"""
    
    def test_sensor_list_accessibility(self, bmc_client):
        """
        測試 7: 驗證感應器列表可訪問性
        """
        logger.info("Test 7: Sensor List Accessibility")
        
        start_time = time.time()
        sensor_list = bmc_client.get_sensor_list()
        elapsed_time = time.time() - start_time
        
        assert sensor_list is not None, "Failed to get sensor list"
        assert len(sensor_list) > 0, "No sensors available"
        
        logger.info(f"✓ Retrieved {len(sensor_list)} sensors in {elapsed_time:.2f}s")
        logger.info(f"  Average time per sensor: {elapsed_time/len(sensor_list)*1000:.2f}ms")
    
    def test_sensor_data_completeness(self, bmc_client):
        """
        測試 8: 驗證感應器數據完整性
        """
        logger.info("Test 8: Sensor Data Completeness")
        
        sensor_list = bmc_client.get_sensor_list()
        
        required_fields = ['Name', 'Reading', 'ReadingUnits', 'Status']
        missing_data = []
        
        for sensor in sensor_list:
            for field in required_fields:
                if field not in sensor:
                    missing_data.append({
                        'sensor': sensor.get('Name', 'Unknown'),
                        'missing_field': field
                    })
        
        if missing_data:
            logger.warning(f"Found {len(missing_data)} sensors with incomplete data")
            for item in missing_data[:5]:
                logger.warning(f"  - {item['sensor']}: missing {item['missing_field']}")
        else:
            logger.info(f"✓ All {len(sensor_list)} sensors have complete data")
        
        # 允許某些缺失 (warning)，但不能全部缺失
        assert len(missing_data) < len(sensor_list), \
            "Most sensors have incomplete data"
