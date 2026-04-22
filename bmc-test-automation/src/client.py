import requests
import json
import time
import logging
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from typing import Optional, Dict, Any

# 設定 logger
logger = logging.getLogger(__name__)

# 關閉 SSL 警告訊息（僅開發環境使用）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RedfishClient:
    def __init__(self, base_url: str, auth: Optional[tuple], timeout: int = 10, verify_ssl: bool = False):
        """
        初始化 Redfish Client
        
        Args:
            base_url: BMC 基礎 URL (例如：https://192.168.100.60)
            auth: (username, password) 認證資訊
            timeout: 請求超時時間（秒）
            verify_ssl: 是否驗證 SSL 憑證（預設 False，因為 BMC 通常使用自簽名憑證）
        """
        self.base_url = base_url.rstrip('/')
        self.auth = auth
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.token = None
        self.chassis_id = "1"  # 預設 Chassis Instance
        self._is_closed = False
        
        # 建立 Session 並配置連線池
        self.session = requests.Session()
        
        # 配置連線池限制 (最多 10 個連線)
        adapter = HTTPAdapter(
            pool_connections=1,
            pool_maxsize=1,
            max_retries=Retry(
                total=3,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504]
            )
        )
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)
        
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def set_chassis_id(self, chassis_id: str):
        """設定 Chassis Instance ID"""
        self.chassis_id = chassis_id
        logger.info(f"Chassis ID set to: {self.chassis_id}")

    def login(self) -> bool:
        """進行登入並取得 Session Token"""
        try:
            # 根據 GIGABYTE Redfish API Spec
            login_url = f"{self.base_url}/redfish/v1/SessionService/Sessions"
            
            # 準備登入資料
            login_data = {
                "UserName": self.auth[0],
                "Password": self.auth[1]
            }
            
            # 嘗試方法 1: 使用 Basic Auth + JSON Body (某些版本的 GIGABYTE BMC 要求)
            from requests.auth import HTTPBasicAuth
            basic_auth = HTTPBasicAuth(self.auth[0], self.auth[1])
            
            response = self.session.post(
                login_url, 
                json=login_data,
                auth=basic_auth,
                verify=self.verify_ssl,
                timeout=self.timeout
            )
            
            logger.debug(f"Login response status: {response.status_code}")
            logger.debug(f"Login response headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                # 成功登入，取得 Session Location
                session_location = response.headers.get('Location', '')
                logger.info(f"Login successful. Session: {session_location}")
                
                # 嘗試取得 Token
                try:
                    response_data = response.json()
                    token = response_data.get('token')
                    if token:
                        logger.info(f"Token obtained: {token[:20]}...")
                        self.session.headers.update({"Authorization": f"Bearer {token}"})
                        self.token = token
                        return True
                except Exception as e:
                    logger.debug(f"No token in response: {e}")
                
                # 如果沒有 token，使用 Basic Auth
                self.session.headers.update({"Authorization": f"Basic {self._encode_auth()}"})
                return True
            else:
                logger.error(f"Login failed with status code {response.status_code}. Response: {response.text[:300]}")
                # 即使登入失敗，仍然設定 Basic Auth 作為後備
                self.session.headers.update({"Authorization": f"Basic {self._encode_auth()}"})
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            # 後備方案：設定 Basic Auth
            self.session.headers.update({"Authorization": f"Basic {self._encode_auth()}"})
            return False

    def _encode_auth(self) -> str:
        """編碼認證資訊為 Base64"""
        import base64
        auth_string = f"{self.auth[0]}:{self.auth[1]}"
        return base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    def _get_with_retry(self, url: str, retries: int = 3) -> Optional[requests.Response]:
        """GET 重試邏輯"""
        from requests.auth import HTTPBasicAuth
        basic_auth = HTTPBasicAuth(self.auth[0], self.auth[1])
        
        for i in range(retries):
            try:
                response = self.session.get(
                    url, 
                    auth=basic_auth,
                    verify=self.verify_ssl,
                    timeout=self.timeout
                )
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Too Many Requests
                    logger.warning("Rate limited. Waiting...")
                    time.sleep(1)
                    continue
                elif response.status_code == 401:  # Unauthorized
                    logger.warning("Session expired or unauthorized. Attempting to re-login...")
                    if self.login():
                        continue
                    else:
                        logger.error("Re-login failed.")
                        return None
                else:
                    logger.warning(f"GET {url} returned {response.status_code}. Response: {response.text[:200]}")
                    return response
            except Exception as e:
                logger.warning(f"GET {url} failed with error: {e}. Retry {i+1}/{retries}.")
                time.sleep(0.5)
        return None

    def get(self, path: str) -> Optional[requests.Response]:
        """執行 GET request，並記錄回應"""
        full_url = f"{self.base_url}{path}"
        logger.debug(f"GET {full_url}")
        res = self._get_with_retry(full_url)
        if res is not None:
            logger.debug(f"Response: {res.status_code} ({res.text[:200]}...).")
        return res

    def save_response(self, path: str, response: requests.Response, filename: str) -> bool:
        """儲存 response 為 JSON 檔案"""
        try:
            with open(filename, "w") as f:
                json.dump(response.json(), f, indent=2)
            logger.info(f"Saved response to {filename}.")
            return True
        except Exception as e:
            logger.error(f"Save response failed: {e}.")
            return False

    def get_sensor_list(self) -> Optional[list]:
        """
        取得所有 sensor 的詳細信息（包含讀數、單位、狀態等）
        根據 GIGABYTE Redfish API Spec: /redfish/v1/Chassis/{instance}/Sensors
        """
        url = f"/redfish/v1/Chassis/Self/Sensors"  # 使用 Self 作為自動識別
        resp = self.get(url)
        if resp is None or resp.status_code != 200:
            logger.error(f"Failed to fetch sensor list from {url}.")
            return None
        
        data = resp.json()
        sensors = []
        
        # 處理 Members 陣列
        if "Members" in data:
            for member in data["Members"]:
                sensor_ref = member.get("@odata.id", "")
                if sensor_ref:
                    try:
                        # 取得每個感應器的詳細資訊
                        sensor_detail_resp = self.get(sensor_ref)
                        if sensor_detail_resp and sensor_detail_resp.status_code == 200:
                            sensor_detail = sensor_detail_resp.json()
                            sensor_obj = {
                                'Name': sensor_detail.get('Name', 'N/A'),
                                'Reading': sensor_detail.get('Reading', None),
                                'ReadingUnits': sensor_detail.get('ReadingUnits', 'N/A'),
                                'Status': sensor_detail.get('Status', {}).get('Health', 'N/A'),
                                '@odata.id': sensor_ref
                            }
                            sensors.append(sensor_obj)
                        else:
                            logger.debug(f"Failed to fetch sensor details from {sensor_ref}")
                    except Exception as e:
                        logger.debug(f"Error fetching sensor {sensor_ref}: {e}")
        
        logger.info(f"Found {len(sensors)} sensors.")
        return sensors

    def get_sensor_value(self, sensor_name: str) -> Optional[float]:
        """
        取得特定 sensor 的數值
        根據 GIGABYTE Redfish API Spec: /redfish/v1/Chassis/{instance}/Sensors/{instance}
        """
        url = f"/redfish/v1/Chassis/{self.chassis_id}/Sensors/{sensor_name}"
        resp = self.get(url)
        if resp is None or resp.status_code != 200:
            logger.error(f"Failed to fetch sensor {sensor_name} from {url}.")
            return None
        
        data = resp.json()
        value = data.get("Reading")  # GIGABYTE 使用 Reading 而非 Value
        if value is None:
            value = data.get("Value")  # 相容性檢查
        
        logger.info(f"Sensor {sensor_name}: {value}")
        return value

    def get_temperature_sensors(self) -> Optional[list]:
        """取得溫度感應器清單"""
        url = f"/redfish/v1/Chassis/{self.chassis_id}/Thermal/Temperatures"
        resp = self.get(url)
        if resp is None or resp.status_code != 200:
            logger.error(f"Failed to fetch temperature sensors from {url}.")
            return None
        
        data = resp.json()
        temperatures = []
        if "Members" in data:
            for member in data["Members"]:
                temp_info = {
                    "name": member.get("Name", "Unknown"),
                    "value": member.get("Temperature", member.get("Reading")),
                    "status": member.get("Status", {})
                }
                temperatures.append(temp_info)
        
        return temperatures

    def get_voltage_sensors(self) -> Optional[list]:
        """取得電壓感應器清單"""
        url = f"/redfish/v1/Chassis/{self.chassis_id}/Power/Voltages"
        resp = self.get(url)
        if resp is None or resp.status_code != 200:
            logger.error(f"Failed to fetch voltage sensors from {url}.")
            return None
        
        data = resp.json()
        voltages = []
        if "Members" in data:
            for member in data["Members"]:
                voltage_info = {
                    "name": member.get("Name", "Unknown"),
                    "value": member.get("Voltage", member.get("Reading")),
                    "status": member.get("Status", {})
                }
                voltages.append(voltage_info)
        
        return voltages

    def get_fan_sensors(self) -> Optional[list]:
        """取得風扇感應器清單"""
        url = f"/redfish/v1/Chassis/{self.chassis_id}/Thermal/Fans"
        resp = self.get(url)
        if resp is None or resp.status_code != 200:
            logger.error(f"Failed to fetch fan sensors from {url}.")
            return None
        
        data = resp.json()
        fans = []
        if "Members" in data:
            for member in data["Members"]:
                fan_info = {
                    "name": member.get("Name", "Unknown"),
                    "value": member.get("Reading", member.get("SpeedRPM")),
                    "status": member.get("Status", {})
                }
                fans.append(fan_info)
        
        return fans

    def logout(self):
        """登出並清除 Session"""
        try:
            if self.token:
                session_url = f"{self.base_url}/redfish/v1/SessionService/Sessions"
                self.session.delete(session_url, verify=self.verify_ssl)
                logger.info("Logged out successfully.")
        except Exception as e:
            logger.error(f"Logout error: {e}")
        finally:
            self.token = None
            self.session.close()
            self._is_closed = True

    def close(self):
        """明確關閉連線"""
        if not self._is_closed:
            self.logout()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False

    def __del__(self):
        """析構函數 - 確保連線被清理"""
        try:
            if not self._is_closed:
                self.close()
        except Exception as e:
            logger.debug(f"Error in __del__: {e}")
