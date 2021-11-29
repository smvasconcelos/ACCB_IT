# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['app.py'],
    pathex=['D:\\Uesc\\Scrapper\\web\\ACCB\\Lib\\flask_material\\templates\\material'],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static'), ('schema.sql', '.'), ('itabuna.json', '.'), ('ilheus.json', '.')],
    hiddenimports=[
    'flask_material',
    ],
    hookspath=["."],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_bootlocale'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ACCB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon='logo.ico',
)
