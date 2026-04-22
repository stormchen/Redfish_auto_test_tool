#!/usr/bin/env python3
"""
直接 BMC 連線測試腳本
"""
import sys
import os
import requests
import urllib3
import json
import time

# 關閉 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_bmc_connection():
    """測試 BMC 直接連線"""
    # BMC 設定
    BMC_URL = "https://192.168.100.60"
    USERNAME = "admin"
    PASSWORD = "password"
    
    # 初始化變數用於 finally 塊中使用
    session = None
    session_location = None
    
    print("=" * 60)
    print("開始 BMC 直接連線測試")
    print(f"BMC URL: {BMC_URL}")
    print(f"使用者: {USERNAME}")
    print("=" * 60)
    
    try:
        # 建立 session
        session = requests.Session()
        session.verify = False  # 禮用 SSL 驗證
        
        # 測試基本連線
        print("\n[1/4] 測試基本連線...")
        resp = session.get(f"{BMC_URL}/redfish/v1/", timeout=10)
        print(f"狀態碼: {resp.status_code}")
        if resp.status_code == 200:
            print("基本連線成功")
        else:
            print("基本連線失敗")
            return False
            
        # 測試登入
        print("\n[2/4] 測試登入...")
        login_url = f"{BMC_URL}/redfish/v1/SessionService/Sessions"
        login_data = {
            "UserName": USERNAME,
            "Password": PASSWORD
        }
        
        # 嘗試登入 - 使用 Basic Authentication
        from requests.auth import HTTPBasicAuth
        auth = HTTPBasicAuth(USERNAME, PASSWORD)
        login_resp = session.post(login_url, json=login_data, timeout=10, auth=auth)
        
        print(f"登入狀態碼: {login_resp.status_code}")
        print(f"登入回應頭: {dict(login_resp.headers)}")
        
        # 檢查登入是否成功
        if login_resp.status_code == 201:
            print("登入成功")
            # 取得 Session Location 和 X-Auth-Token (在 Headers 中)
            session_location = login_resp.headers.get('Location', '')
            auth_token = login_resp.headers.get('X-Auth-Token', '')
            
            if session_location:
                print(f"Session Location: {session_location}")
            if auth_token:
                print(f"取得 X-Auth-Token: {auth_token[:20]}...")
                # 在後續請求中使用 X-Auth-Token header
                session.headers.update({"X-Auth-Token": auth_token})
        else:
            print(f"登入失敗: {login_resp.text[:300]}")
            # 即使登入失敗，仍嘗試使用 Basic Auth 繼續
            session.headers.update({"Authorization": f"Basic {auth}"})
            
        # 測試取得系統資訊
        print("\n[3/4] 測試取得系統資訊...")
        sys_resp = session.get(f"{BMC_URL}/redfish/v1/Systems/1", timeout=10)
        print(f"系統狀態碼: {sys_resp.status_code}")
        if sys_resp.status_code == 200:
            print("系統資訊取得成功")
            sys_data = sys_resp.json()
            print(f"系統名稱: {sys_data.get('Name', 'N/A')}")
            print(f"製造商: {sys_data.get('Manufacturer', 'N/A')}")
        else:
            print("系統資訊取得失敗")
            
        # 測試取得感應器清單
        print("\n[4/4] 測試取得感應器清單...")
        # 修改：修正 URI 從 Chassis/1/Sensors 為 Chassis/Self/Sensors
        sensor_url = f"{BMC_URL}/redfish/v1/Chassis/Self/Sensors"
        sensor_resp = session.get(sensor_url, timeout=10)
        print(f"感應器狀態碼: {sensor_resp.status_code}")
        sensor_results = []
        
        if sensor_resp.status_code == 200:
            print("感應器清單取得成功")
            sensor_data = sensor_resp.json()
            members = sensor_data.get('Members', [])
            print(f"找到 {len(members)} 個感應器\n")
            
            # 遍歷並詳細輸出每個感應器
            for idx, sensor_member in enumerate(members, 1):
                sensor_ref = sensor_member.get('@odata.id', '')
                if sensor_ref:
                    try:
                        # 獲取個別感應器的詳細資訊
                        sensor_detail_resp = session.get(f"{BMC_URL}{sensor_ref}", timeout=10)
                        if sensor_detail_resp.status_code == 200:
                            sensor_detail = sensor_detail_resp.json()
                            sensor_name = sensor_detail.get('Name', 'N/A')
                            sensor_reading = sensor_detail.get('Reading', 'N/A')
                            sensor_unit = sensor_detail.get('ReadingUnits', 'N/A')
                            sensor_status = sensor_detail.get('Status', {}).get('Health', 'N/A')
                            
                            output = f"  [{idx:2d}] {sensor_name:<30} 值: {str(sensor_reading):>10} {sensor_unit:<10} 狀態: {sensor_status}"
                            print(output)
                            sensor_results.append({
                                'name': sensor_name,
                                'reading': sensor_reading,
                                'unit': sensor_unit,
                                'status': sensor_status
                            })
                        else:
                            print(f"  [{idx:2d}] 無法獲取詳細資訊 (狀態碼: {sensor_detail_resp.status_code})")
                    except Exception as e:
                        print(f"  [{idx:2d}] 獲取詳細資訊失敗: {str(e)[:50]}")
            
            # 生成報告文件
            report_path = "reports/html/sensor_report.txt"
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("BMC 感應器測試報告\n")
                f.write("=" * 80 + "\n")
                f.write(f"測試時間: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"BMC URL: {BMC_URL}\n")
                f.write(f"總感應器數: {len(sensor_results)}\n")
                f.write("=" * 80 + "\n\n")
                
                for idx, sensor in enumerate(sensor_results, 1):
                    f.write(f"[{idx:2d}] {sensor['name']}\n")
                    f.write(f"     讀數: {sensor['reading']} {sensor['unit']}\n")
                    f.write(f"     狀態: {sensor['status']}\n\n")
            
            print(f"\n感應器詳細報告已儲存至: {report_path}")
        else:
            print("感應器清單取得失敗")
            
        print("\n" + "=" * 60)
        print("所有測試完成")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 嘗試登出（如果有有效的 session location）
        try:
            if 'session_location' in locals() and session_location:
                logout_url = f"{BMC_URL}{session_location}" if session_location.startswith('/') else f"{BMC_URL}/{session_location}"
                print(f"\n[登出] 刪除 Session: {session_location}...")
                logout_resp = session.delete(logout_url, timeout=5)
                print(f"登出狀態碼: {logout_resp.status_code}")
        except Exception as logout_error:
            print(f"登出失敗: {logout_error}")
        
        # 關閉 session
        try:
            session.close()
        except:
            pass
        
        # 強制釋放所有連線
        import gc
        gc.collect()

def main():
    """主函數"""
    print("執行 BMC 測試，將控制連線數量不超過 15 個且每次連線間加入延遲")
    
    # 控制連線數量不超過 15 個
    max_connections = 15
    
    # 執行測試
    success = test_bmc_connection()
    
    # 加入較長延遲
    if success:
        print("測試成功，等待 10 秒...")
        time.sleep(10)
    else:
        print("測試失敗，等待 10 秒...")
        time.sleep(10)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)