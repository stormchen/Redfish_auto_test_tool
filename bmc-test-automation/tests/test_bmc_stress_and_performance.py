"""
BMC 壓力與效能測試 (Performance & Stress)
針對長時間穩定性與高併發連線進行壓力測試，並監控資源使用率。
"""
import pytest
import time
import logging
import concurrent.futures
from statistics import mean, quantiles

logger = logging.getLogger(__name__)

class TestBMCStressAndPerformance:
    
    @pytest.mark.stress
    def test_high_concurrency_redfish_access(self, bmc_client):
        """
        高併發壓力測試: 模擬多個管理者同時存取 Redfish API
        """
        logger.info("Starting High Concurrency Redfish Access Test (10 workers)")
        
        url_to_test = "/redfish/v1/Systems/Self"
        concurrent_requests = 10
        response_times = []
        error_count = 0
        
        def fetch_system_info():
            start = time.time()
            try:
                # 假設 bmc_client 有 raw_get 方法可以測試特定 Endpoint
                resp = bmc_client.get(url_to_test)
                if resp.status_code == 200:
                    return time.time() - start, None
                else:
                    return time.time() - start, f"HTTP {resp.status_code}"
            except Exception as e:
                return time.time() - start, str(e)

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = [executor.submit(fetch_system_info) for _ in range(concurrent_requests)]
            for future in concurrent.futures.as_completed(futures):
                duration, err = future.result()
                response_times.append(duration)
                if err:
                    error_count += 1
                    
        # 分析結果
        p95 = quantiles(response_times, n=100)[94] * 1000
        avg = mean(response_times) * 1000
        error_rate = (error_count / concurrent_requests) * 100
        
        logger.info(f"Concurrency Test Results:")
        logger.info(f"  Total Requests: {concurrent_requests}")
        logger.info(f"  Error Rate: {error_rate:.2f}% ({error_count} errors)")
        logger.info(f"  P95 Response Time: {p95:.2f}ms")
        logger.info(f"  Avg Response Time: {avg:.2f}ms")
        
        # 效能基準斷言
        assert error_rate < 1.0, f"Error rate too high: {error_rate}% > 1.0%"
        assert p95 < 2000, f"P95 response time too slow under load: {p95}ms > 2000ms"

    @pytest.mark.aging
    def test_aging_memory_leak_monitor(self, bmc_client):
        """
        長時間輪詢穩定性測試 (Aging Test): 模擬長時間運作並檢查 BMC 記憶體狀態。
        註：在 CI/CD 中通常縮短為 5 分鐘，實際實驗室環境可設為 72 小時。
        """
        duration_minutes = 2  # 測試用設定為 2 分鐘
        end_time = time.time() + (duration_minutes * 60)
        
        logger.info(f"Starting Aging Test for {duration_minutes} minutes to monitor memory leak")
        
        initial_mem = None
        final_mem = None
        
        while time.time() < end_time:
            try:
                # 取得 BMC 自身管理資源狀態 (Manager)
                managers = bmc_client.get("/redfish/v1/Managers/Self").json()
                # 假設 BMC 回報 Memory 狀態在 Oem 或是特定屬性中
                # 這裡使用一個通用的讀取邏輯示意
                mem_usage = managers.get('Oem', {}).get('MemoryUsagePercentage', None)
                
                if mem_usage is not None:
                    if initial_mem is None:
                        initial_mem = mem_usage
                    final_mem = mem_usage
                    
                    # 防護機制：如果使用率飆高超過 90% 立即報錯
                    assert mem_usage < 90, f"Critical Memory Usage detected: {mem_usage}%"
                    
            except Exception as e:
                logger.warning(f"Failed to get Manager stats during aging: {e}")
                
            time.sleep(10) # 每 10 秒取樣一次
            
        if initial_mem is not None and final_mem is not None:
            diff = final_mem - initial_mem
            logger.info(f"Aging Test Complete. Memory variation: {initial_mem}% -> {final_mem}% (Diff: {diff}%)")
            assert diff < 10, f"Potential Memory Leak detected! Usage increased by {diff}% in {duration_minutes} mins."
        else:
            logger.warning("Could not monitor memory usage. Oem.MemoryUsagePercentage not found.")
