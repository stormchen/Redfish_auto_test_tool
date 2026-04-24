"""
AI 伺服器專屬情境邏輯驗證 (GB200/GB300 散熱與功耗特性)
"""
import pytest
import logging
import time

logger = logging.getLogger(__name__)

class TestAIServerCoolingAndPower:
    
    @pytest.mark.ai_server
    def test_liquid_cooling_pump_response(self, bmc_client):
        """
        測試 AI 伺服器高負載下的水冷幫浦與風扇聯動策略
        情境: 模擬或偵測 GPU 高溫時，Cooling 系統是否如期拉高轉速/流速
        """
        logger.info("Testing Liquid Cooling & Fan response strategy for AI Server")
        
        # 1. 取得所有 GPU 溫度與散熱設備狀態
        sensors = bmc_client.get_sensor_list()
        gpu_temps = [s for s in sensors if 'GPU' in s.get('Name', '').upper() and 'TEMP' in s.get('Name', '').upper()]
        cooling_fans = [s for s in sensors if 'FAN' in s.get('Name', '').upper() or 'PUMP' in s.get('Name', '').upper()]
        
        if not gpu_temps or not cooling_fans:
            pytest.skip("No GPU temperature or Cooling sensors found. Not an AI Server environment.")
            
        # 2. 找出最熱的 GPU
        max_gpu = max(gpu_temps, key=lambda x: x.get('Reading', 0))
        max_temp = max_gpu.get('Reading', 0)
        logger.info(f"Hottest GPU: {max_gpu.get('Name')} at {max_temp}°C")
        
        # 3. 散熱策略邏輯驗證 (Reality Checker)
        # 規則：如果 GPU 溫度 > 85度，所有 Pump 轉速必須 > 80% (假設的 AI Server Spec)
        if max_temp > 85:
            logger.info("High thermal load detected. Verifying cooling strategy...")
            failed_coolers = []
            for fan in cooling_fans:
                reading = fan.get('Reading', 0)
                # 假設滿載為 100% 或 RPM 轉換
                if reading < 80: # 簡化為 80 單位
                    failed_coolers.append(fan.get('Name'))
            
            if failed_coolers:
                pytest.fail(f"Cooling strategy failure! GPU is at {max_temp}°C but coolers are under-performing: {failed_coolers}")
        else:
            logger.info("GPU temperature is normal. Dynamic cooling strategy test passed (baseline).")
            
    @pytest.mark.ai_server
    def test_power_limit_boundary(self, bmc_client):
        """
        電源控制邊界測試 (Power Limit Boundary)
        驗證當系統嘗試設定異常的 Power Limit 時，BMC 是否能正確阻擋或回應
        """
        logger.info("Testing Power Limit Boundary conditions")
        
        # 假設取得 Power Limit API (Power/PowerControl)
        # 這裡僅實作測試邏輯的概念展示
        power_url = "/redfish/v1/Chassis/Self/Power"
        
        try:
            # 獲取目前設定
            resp = bmc_client.get(power_url)
            if resp.status_code != 200:
                pytest.skip("Power Control not supported or not accessible.")
                
            # 嘗試寫入異常高的 Power Limit (超出 GB300 規格)
            invalid_power_payload = {
                "PowerControl": [
                    {
                        "PowerLimit": {
                            "LimitInWatts": 999999  # 超過邊界
                        }
                    }
                ]
            }
            
            # 使用 PATCH 進行修改
            patch_resp = bmc_client.patch(power_url, json=invalid_power_payload)
            
            # 現實查核: 系統必須拒絕這個不合理的設定 (通常回傳 400 Bad Request)
            assert patch_resp.status_code in [400, 422], f"BMC accepted invalid power limit! Status: {patch_resp.status_code}"
            logger.info("✓ BMC successfully rejected boundary-breaking power limit.")
            
        except AttributeError:
             pytest.skip("BMC client missing HTTP methods for boundary test")
