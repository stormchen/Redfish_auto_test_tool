#!/usr/bin/env python3
"""
簡單 BMC 連線測試腳本
僅測試基本連線與登入功能
"""
import sys
import requests
import urllib3
import json
import time
from contextlib import contextmanager

# 關閉 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@contextmanager
def bmc_session(bmc_url, username, password):
    """
    BMC 連線管理器
    自動處理連線建立與釋放
    """
    session = None
    try:
        session = requests.Session()
        session.verify = False  # 禮用 SSL 驗證
        
        # 建立連線
        resp = session.get(f"{bmc_url}/redfish/v1/", timeout=10)
        if resp.status_code != 200:
            raise Exception(f"連線失敗: {resp.status_code}")
            
        # 登入
        login_url = f"{bmc_url}/redfish/v1/SessionService/Sessions"
        login_data = {
            "UserName": username,
            "Password": password
        }
        
        # 使用 Basic Auth
        from requests.auth import HTTPBasicAuth
        auth = HTTPBasicAuth(username, password)
        login_resp = session.post(login_url, json=login_data, auth=auth, timeout=10)
        
        if login_resp.status_code != 201:
            raise Exception(f"登入失敗: {login_resp.status_code}")
            
        yield session
        
    except Exception as e:
        print(f"連線處理失敗: {e}")
        raise
    finally:
        # 關閉連線
        if session:
            session.close()

def simple_bmc_test():
    """簡單 BMC 測試"""
    # BMC 設定
    BMC_URL = "https://192.168.100.60"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("=" * 50)
    print("簡單 BMC 連線測試")
    print(f"BMC URL: {BMC_URL}")
    print(f"使用者: {USERNAME}")
    print("=" * 50)
    
    try:
        # 使用上下文管理器處理連線
        with bmc_session(BMC_URL, USERNAME, PASSWORD) as session:
            print("\n[1/3] 測試基本連線...")
            resp = session.get(f"{BMC_URL}/redfish/v1/", timeout=10)
            print(f"狀態碼: {resp.status_code}")
            if resp.status_code == 200:
                print("基本連線成功")
            else:
                print("基本連線失敗")
                return False
                
            print("\n[2/3] 測試登入...")
            login_url = f"{BMC_URL}/redfish/v1/SessionService/Sessions"
            login_data = {
                "UserName": USERNAME,
                "Password": PASSWORD
            }
            
            login_resp = session.post(login_url, json=login_data, timeout=10)
            print(f"登入狀態碼: {login_resp.status_code}")
            if login_resp.status_code == 201:
                print("登入成功")
                return True
            else:
                print("登入失敗")
                print(f"錯誤訊息: {login_resp.text[:200] if len(login_resp.text) > 200 else login_resp.text}")
                return False
                
    except Exception as e:
        print(f"測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函數"""
    print("執行簡單 BMC 測試以確認連線與權限")
    
    # 執行測試
    success = simple_bmc_test()
    
    # 加入延遲
    print("測試完成，等待 5 秒...")
    time.sleep(5)
    
    if success:
        print("\n測試成功：連線與帳號密碼正常")
    else:
        print("\n測試失敗：連線或帳號密碼異常")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)