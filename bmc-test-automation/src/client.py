import requests
import json
import time
import logging

from typing import Optional, Dict, Any

# 設定 logger
logger = logging.getLogger(__name__)

class RedfishClient:
    def __init__(self, base_url: str, auth: Optional[tuple], timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.auth = auth
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.token = None

    def login(self) -> bool:
        """進行登入並取得 Token"""
        try:
            login_url = f"{self.base_url}/redfish/v1/SessionService/ Sessions"
            response = self.session.post(login_url, auth=self.auth, timeout=self.timeout)
            if response.status_code != 201:
                logger.error(f"Login failed with status code {response.status_code}.")
                return False
            data = response.json()
            self.token = data['token']
            self.session.headers.update({"Authorization": f"Bearer {self.token}"}) 
            logger.info("Login successful with token.")
            return True
        except Exception as e:
            logger.error(f"Login error: {e}.")
            return False

    def _get_with_retry(self, url: str, retries: int = 3) -> Optional[requests.Response]:
        """GET 重試邏輯"""
        for i in range(retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Too Many Requests
                    logger.warning("Rate limited. Waiting...")
                    time.sleep(1)
                    continue
                else:
                    logger.warning(f"GET {url} returned {response.status_code}.")
            except Exception as e:
                logger.warning(f"GET {url} failed with error: {e}. Retry {i}/{retries - 1}.")
                time.sleep(0.5)
        return None

    def get(self, path: str) -> Optional[requests.Response]:
        """執行 GET request，並記錄回應"""
        full_url = f"{self.base_url}{path}"
        logger.debug(f"GET {full_url}")
        res = self._get_with_retry(full_url)
        if res is not None:
            logger.debug(f"Response: {res.status_code} ({res.text[:200]}...)")
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