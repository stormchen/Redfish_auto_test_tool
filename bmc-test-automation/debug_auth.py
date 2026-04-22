#!/usr/bin/env python3
"""
BMC 認證調試腳本
用於診斷登入問題
"""
import sys
import requests
import urllib3
import json
from requests.auth import HTTPBasicAuth

# 關閉 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def debug_auth():
    """調試認證流程"""
    BMC_URL = "https://192.168.100.60"
    USERNAME = "admin"
    PASSWORD = "password"
    
    print("=" * 70)
    print("BMC 認證調試")
    print("=" * 70)
    
    session = requests.Session()
    session.verify = False
    
    # 步驟 1: 基本連線測試
    print("\n[步驟 1] 基本連線測試")
    print("-" * 70)
    try:
        resp = session.get(f"{BMC_URL}/redfish/v1/", timeout=10)
        print(f"狀態碼: {resp.status_code}")
        print(f"回應頭:\n{json.dumps(dict(resp.headers), indent=2)[:500]}")
        if resp.status_code == 200:
            print("✓ 基本連線成功")
        else:
            print("✗ 基本連線失敗")
    except Exception as e:
        print(f"✗ 連線失敗: {e}")
        return
    
    # 步驟 2: 嘗試不同的認證方法
    print("\n[步驟 2] 嘗試方法 A: 使用 Basic Auth 在 HTTP header 中")
    print("-" * 70)
    try:
        login_url = f"{BMC_URL}/redfish/v1/SessionService/Sessions"
        login_data = {
            "UserName": USERNAME,
            "Password": PASSWORD
        }
        
        auth = HTTPBasicAuth(USERNAME, PASSWORD)
        resp = session.post(login_url, json=login_data, auth=auth, timeout=10)
        
        print(f"狀態碼: {resp.status_code}")
        print(f"回應頭:\n{json.dumps(dict(resp.headers), indent=2)[:500]}")
        print(f"回應體 (前 500 字元):\n{resp.text[:500]}")
        
        if resp.status_code == 201:
            print("✓ 登入成功 (方法 A)")
            try:
                resp_json = resp.json()
                print(f"回應 JSON:\n{json.dumps(resp_json, indent=2)}")
            except:
                pass
        else:
            print(f"✗ 登入失敗 (方法 A) - 狀態碼: {resp.status_code}")
    except Exception as e:
        print(f"✗ 方法 A 失敗: {e}")
    
    # 步驟 3: 嘗試不使用 Basic Auth
    print("\n[步驟 3] 嘗試方法 B: 只發送 JSON body，不使用 Basic Auth")
    print("-" * 70)
    try:
        session2 = requests.Session()
        session2.verify = False
        
        login_url = f"{BMC_URL}/redfish/v1/SessionService/Sessions"
        login_data = {
            "UserName": USERNAME,
            "Password": PASSWORD
        }
        
        resp = session2.post(login_url, json=login_data, timeout=10)
        
        print(f"狀態碼: {resp.status_code}")
        print(f"回應頭:\n{json.dumps(dict(resp.headers), indent=2)[:500]}")
        print(f"回應體 (前 500 字元):\n{resp.text[:500]}")
        
        if resp.status_code == 201:
            print("✓ 登入成功 (方法 B)")
            try:
                resp_json = resp.json()
                print(f"回應 JSON:\n{json.dumps(resp_json, indent=2)}")
            except:
                pass
        else:
            print(f"✗ 登入失敗 (方法 B) - 狀態碼: {resp.status_code}")
            
        session2.close()
    except Exception as e:
        print(f"✗ 方法 B 失敗: {e}")
    
    # 步驟 4: 檢查 Redfish 版本與服務資訊
    print("\n[步驟 4] 檢查 Redfish 版本")
    print("-" * 70)
    try:
        resp = session.get(f"{BMC_URL}/redfish/", timeout=10)
        print(f"狀態碼: {resp.status_code}")
        if resp.status_code == 200:
            try:
                data = resp.json()
                print(f"Redfish 服務:\n{json.dumps(data, indent=2)}")
            except:
                print(f"回應: {resp.text[:300]}")
    except Exception as e:
        print(f"✗ 檢查失敗: {e}")
    
    session.close()
    
    # 步驟 5: 建議
    print("\n" + "=" * 70)
    print("建議:")
    print("=" * 70)
    print("""
1. 檢查 BMC IP 地址是否正確: 192.168.100.60
2. 檢查使用者名稱和密碼是否正確: admin / password
3. 確認 BMC 是否支援 Redfish API
4. 檢查 BMC 的防火牆設定，確保允許 HTTPS 連線
5. 嘗試使用 IPMI 工具驗證連線:
   ipmitool -H 192.168.100.60 -U admin -P password chassis status
    """)

if __name__ == "__main__":
    debug_auth()
