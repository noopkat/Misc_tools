# -*- mode: python -*-
# example run cmd: `pyinstaller --additional-hooks-dir=hooks/ Maker-Linux.spec`
import os

def Datafiles(*filenames, **kw):
  def datafile(path, strip_path=False):
    parts = path.split('/')
    path = name = os.path.join(*parts)
    if strip_path:
      name = os.path.basename(path)
    return name, path, 'DATA'

  strip_path = kw.get('strip_path', True)
  return TOC(
    datafile(filename, strip_path=strip_path)
    for filename in filenames
    if os.path.isfile(filename))

docfiles = Datafiles('pic.gif', 'pr.hex')

a = Analysis(['Maker.py'],
             pathex=['./'],
             hiddenimports=['intelhex', 'datetime', 'struct', 'math', 'crcmod', 'getopt'],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Maker',
          debug=False,
          strip=None,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               docfiles,
               strip=None,
               upx=True,
               name='Maker')
