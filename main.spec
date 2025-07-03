# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import py_mini_racer

datas = collect_data_files('akshare', includes=['file_fold/calendar.json'])

for root, dirs, files in os.walk('res'):
    if 'AKShare_Output' in dirs:
        dirs.remove('AKShare_Output')

    for file in files:
        src_file = os.path.join(root, file)
        datas.append( (src_file, os.path.dirname(src_file)) )

dylib_file = 'libmini_racer.dylib'
if os.name == "nt":
    dylib_file = 'mini_racer.dll'
dylib_path = os.path.join(os.path.dirname(py_mini_racer.__file__), dylib_file)
icudtl_path = os.path.join(os.path.dirname(py_mini_racer.__file__), 'icudtl.dat')
snapshot_blob_path = os.path.join(os.path.dirname(py_mini_racer.__file__), 'snapshot_blob.bin')
datas.append( (dylib_path, '.') )
datas.append( (icudtl_path, '.') )
datas.append( (snapshot_blob_path, '.') )

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

if os.name == "nt":
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='main',
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
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='main',
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
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='main',
    )
    app = BUNDLE(
        coll,
        name='main.app',
        icon=None,
        bundle_identifier=None,
    )
