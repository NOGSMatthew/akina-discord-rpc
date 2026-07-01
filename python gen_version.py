# generer version.txt
# colle ce code dans un fichier gen_version.py et execute le
from PyInstaller.utils.win32.versioninfo import *

v = VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
  ),
  kids=[
    StringFileInfo([
      StringTable('040C04B0', [
        StringStruct('CompanyName',      'Akina Community'),
        StringStruct('FileDescription',  'Akina RPC Installer'),
        StringStruct('FileVersion',      '1.0.0'),
        StringStruct('InternalName',     'AkinaRPC_Setup'),
        StringStruct('OriginalFilename', 'AkinaRPC_Setup.exe'),
        StringStruct('ProductName',      'Akina RPC'),
        StringStruct('ProductVersion',   '1.0.0'),
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [0x040C, 1200])])
  ]
)

open("version.txt","w").write(str(v))
print("version.txt genere")
