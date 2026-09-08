# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['interface/app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/lucas12364/Desktop/Validador de Telas/logo.png', '.'), ('C:/Users/lucas12364/Desktop/Validador de Telas/logo.ico', '.'), ('C:/Users/lucas12364/Desktop/Validador de Telas/config', 'config')],
    hiddenimports=['main', 'services.login', 'services.checker', 'services.logger', 'services.report', 'services.scanner', 'services.context_manager', 'validators.page_validator', 'config.config', 'config.monitor_config', 'config.context_config'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ScriptCaseMonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:/Users/lucas12364/Desktop/Validador de Telas/logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScriptCaseMonitor',
)
