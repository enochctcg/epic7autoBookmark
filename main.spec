# -*- mode: python ; coding: utf-8 -*-
# 跨平台打包設定: 在哪個系統執行就產出哪個系統的版本 (PyInstaller 不能跨平台編譯)
#   Windows: pyinstaller main.spec  ->  dist/epic7autoBookmark.exe
#   macOS  : pyinstaller main.spec  ->  dist/epic7autoBookmark.app
# config.json 不打包進去, 放在 exe / .app 旁邊讓使用者自行修改。
import sys

from PyInstaller.utils.hooks import collect_data_files

IS_MACOS = sys.platform == "darwin"

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    # adbutils 的 Windows 版內建 adb.exe (adbutils/binaries), 要一起打包才找得到
    datas=[('img', 'img'), ('main.ico', '.')] + collect_data_files('adbutils'),
    hiddenimports=['adbutils.binaries'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if IS_MACOS:
    # macOS: onedir + .app bundle (onefile 的 .app 啟動慢且 PyInstaller 6 已不建議)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='epic7autoBookmark',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='main.ico',  # 需要安裝 Pillow, PyInstaller 會自動轉成 .icns
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=False,
        name='epic7autoBookmark',
    )
    app = BUNDLE(
        coll,
        name='epic7autoBookmark.app',
        icon='main.ico',
        bundle_identifier='com.github.epic7autobookmark',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleDisplayName': '第七史詩刷商店小工具',
        },
    )
else:
    # Windows: 單一 exe, 與原本行為相同
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='epic7autoBookmark',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,  # UPX 壓縮容易被防毒軟體誤判, 關閉
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='main.ico',
    )
