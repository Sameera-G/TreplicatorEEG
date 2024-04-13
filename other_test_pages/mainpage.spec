# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainpage.py'],
    pathex=[],
    binaries=[],
    datas=[('images/*', 'images/'), ('paragraphs/*', 'paragraphs/'), ('firebase/bci-research-77b3d-02a9edb61fd4.json', 'firebase/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='mainpage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
