# epic7autoBookmark

第七史詩自動刷秘密商店的小工具。輸入要花掉的天空石數量，按下開始後，會自動更新商店，看到**聖約書籤**和**神秘書籤**就買。

- 透過 Android ADB 操作模擬器，不會搶滑鼠，視窗可以縮小放著
- 支援 Windows 與 macOS
- 目前不支援國服，國服可以參考 [epic7auto](https://github.com/Wrong-pixel/epic7auto)

---

## 一、使用前準備

### 1. 模擬器設定
- Windows：BlueStacks（理論上全版本通用）
- macOS：BlueStacks Air（Apple Silicon）
- 顯示：**橫向、1920x1080、DPI 240 或 320**（一定要這個解析度，按鈕比對和點擊位置都是以它為準）
- 開啟 ADB：設定 → 進階 → Android調試橋(ADB)，打開後會看到位址，例如 `127.0.0.1:5555`
  - 英文介面：Settings → Advanced → Android Debug Bridge (ADB)

![ADB 設定](https://i.imgur.com/eSamCR3.png)

### 2. 遊戲設定
- 語系選繁中、簡中或英文，並與 `config.json` 的 `e7_language` 相同
- 裝置詳細設定、遊戲詳細設定最好都不勾（推薦只勾高級設定），高畫質套件也測試過可正常運行

### 3. config.json
跟執行檔放在同一個資料夾：

```json
{
    "adb_addr": "127.0.0.1:5555",
    "e7_language": "zh-TW",
    "adb_path": ""
}
```

| 欄位 | 說明 |
|---|---|
| `adb_addr` | 模擬器 ADB 設定頁顯示的位址 |
| `e7_language` | 遊戲語系：繁中 `zh-TW`、簡中 `zh-CN`、英文 `en-US` |
| `adb_path` | 選填，adb 執行檔的完整路徑。留空會自動尋找（優先使用 BlueStacks 自帶的 adb） |

> **出現「錯誤: closed」？** 通常是 adb 版本衝突，把 `adb_path` 指定成 BlueStacks 自帶的 adb：
> - Windows：`"adb_path": "C:\\Program Files\\BlueStacks_nxt\\HD-Adb.exe"`（JSON 裡的反斜線要寫兩個）
> - macOS：`"adb_path": "/Applications/BlueStacks.app/Contents/MacOS/hd-adb"`

---

## 二、使用方式

### Windows
1. 下載 `epic7autoBookmark-windows.zip`，解壓縮到一個資料夾（路徑可以有中文）
2. 確認 `config.json` 設定正確
3. 開啟遊戲，進到**秘密商店**畫面

   ![秘密商店](https://i.imgur.com/KxeSpWM.png)

4. 執行 `epic7autoBookmark.exe`，輸入要使用的天空石數量，按「開始」

> Windows 第一次執行如果跳出「Windows 已保護您的電腦」，按「其他資訊」→「仍要執行」。這是因為執行檔沒有數位簽章，不是病毒；有疑慮可以照下方「自己打包」的步驟自行打包。

### macOS
1. 下載 `epic7autoBookmark-macos.zip` 並解壓縮
2. 確認 `config.json` 設定正確（跟 `epic7autoBookmark.app` 放在同一個資料夾）
3. 開啟遊戲，進到**秘密商店**畫面
4. 第一次開啟：對 `epic7autoBookmark.app` 按右鍵 →「打開」→「打開」（直接點兩下會被 macOS 擋下，因為沒有 Apple 簽章）
5. 輸入要使用的天空石數量，按「開始」

### 說明
- 每 3 個天空石更新一次商店。例如輸入 30 個，會更新 10 次，加上目前這間，總共檢查 11 間商店
- 聖約書籤、神秘書籤出現就會購買，請自行確認金幣足夠（聖約 184,000、神秘 280,000）
- 執行中可以隨時按「停止」

### 出問題時
執行檔旁邊會自動產生 `logs/` 資料夾：
- `logs/epic7-日期-時間.log`：每一步的詳細日誌（截圖、按鈕比對信心值、點擊座標）
- `logs/screenshots/`：找不到按鈕時的當下畫面

回報問題時附上這兩個，比較容易找出原因。最常見的原因是遊戲改版後按鈕樣式變了，需要重新截取 `img/` 裡的按鈕圖片。

---

## 三、打包發布（開發者）

PyInstaller **不能跨平台打包**：Windows 的 exe 一定要在 Windows 上打包，macOS 的 app 一定要在 Mac 上打包。

### 方法 A：GitHub Actions 自動打包（推薦，用 Mac 也能產出 exe）
專案已附 `.github/workflows/build.yml`，會在 GitHub 的雲端 Windows / macOS 機器上同時打包。

1. 把專案推到**自己的** GitHub 倉庫
2. 打包方式二選一：
   - **手動**：GitHub 網頁 → Actions → Build → Run workflow。完成後在該次執行頁面最下方的 Artifacts 下載 `epic7autoBookmark-windows.zip`、`epic7autoBookmark-macos.zip`
   - **發布版本**：推一個 v 開頭的 tag，會自動建立 Release 並附上兩個壓縮檔，直接把 Release 連結給別人即可
     ```bash
     git tag v1.0.0
     git push origin v1.0.0
     ```

壓縮檔內含執行檔、`config.json`、`README.md`、`LICENSE`，解壓縮就能用。

> GitHub 的 `macos-latest` 是 Apple Silicon 機器，打包出的 app 只能在 M 系列晶片的 Mac 上執行。

### 方法 B：在本機打包
需要 Python 3.9 以上。

```bash
# 建立虛擬環境
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS  : source .venv/bin/activate

pip install -r requirements.txt pyinstaller pillow
pyinstaller -y main.spec
```

- Windows：產出 `dist/epic7autoBookmark.exe`
- macOS：產出 `dist/epic7autoBookmark.app`

給別人時，把執行檔和 `config.json` 放在同一個資料夾一起壓縮。`img/` 已經打包進執行檔裡；如果執行檔旁邊也放一份 `img/`，會優先使用旁邊的圖片（方便替換改版後的按鈕圖）。

### 用原始碼執行（開發測試用）
```bash
pip install -r requirements.txt
python main.py
```
macOS 需要另外安裝 adb（`brew install android-platform-tools`，或使用 BlueStacks 自帶的 `hd-adb`）；Windows 不用，adbutils 已內建。

---

## 特別感謝
Raven9527 - 自動點擊派遣功能（遊戲已移除派遣，此功能已拿掉）
