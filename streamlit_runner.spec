# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata, exec_statement
import os

st_file = exec_statement('import streamlit; print(streamlit.__file__)')
st_static_dir = os.path.join(os.path.dirname(st_file),'static')


datas = []
datas += copy_metadata('streamlit')
datas += [(st_static_dir,'./streamlit/static')]


block_cipher = None


a = Analysis(
    ['streamlit_runner.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pyesapi','pyarrow.vendored.version','streamlit.runtime.scriptrunner.magic_funcs'],
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='streamlit_runner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='streamlit_runner',
)
