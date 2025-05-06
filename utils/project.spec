# project.spec

block_cipher = None

a = Analysis(
    ['flv.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'polars', 'PIL', 'programstate', 'btn', 'ui', 'loaders', 'config', 'img', 'tkinter'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FastLogViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Без консоли
    icon=None       # Можно указать свою .ico иконку здесь
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    strip=False,
    upx=True,
    name='FastLogViewer'
)