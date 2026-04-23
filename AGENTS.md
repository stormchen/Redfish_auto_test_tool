調用工具時請使用以下邏輯

禁止使用遞迴式的 ls -R 或 Get-ChildItem -Recurse。

強制截斷： 執行目錄列出時，請務必在 PowerShell 指令後方加上 | Select-Object -First 30。

結構化優先： 優先使用 tree /f /a 並限制深度（例如只顯示兩層），而非列出所有檔案細節。

2. 強制排除清單 (Mandatory Exclusions)
在執行任何搜尋或列出指令時，必須自動排除以下 Windows 或專案開發常見的高冗餘目錄：

.git/, node_modules/, bin/, obj/, .vs/, .vscode/

編譯產物： *.exe, *.dll, *.pdb, *.pyc

日誌與暫存： *.log, tmp/, temp/

3. 建議的 PowerShell 指令範本
當你需要查看目錄時，請改用以下邏輯構建指令：

查看目錄摘要：
powershell -Command "Get-ChildItem | Select-Object Name, LastWriteTime | Select-Object -First 20"

精確搜尋檔案：
powershell -Command "Get-ChildItem -Filter '*關鍵字*' -Recurse | Select-Object FullName"

檢查目錄檔案總數（先行評估）：
powershell -Command "(Get-ChildItem).Count"

4. 回覆準則
量大時先報數： 若目錄內檔案超過 50 個，請先回傳：「該目錄共有 X 個檔案，為避免 Context 溢位，我僅列出前 20 個項目或特定類型的檔案...」。

路徑處理： 在 Windows 下路徑請務必使用反斜線 \ 並注意空格路徑需加引號。