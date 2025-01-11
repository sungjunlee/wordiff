import PyInstaller.__main__
import sys
import platform
from pathlib import Path
from wordiff.version import VERSION

def get_icon_path():
    """OS별 아이콘 파일 경로를 반환합니다."""
    assets_dir = Path('assets')
    system = platform.system().lower()
    
    icon_files = {
        'windows': assets_dir / 'icon.ico',
        'darwin': assets_dir / 'icon.icns',
        'linux': assets_dir / 'icon.png'
    }
    
    return str(icon_files.get(system, ''))

def build():
    # 기본 빌드 옵션
    args = [
        'wordiff/gui.py',                 # 메인 스크립트
        '--name=wordiff',                 # 출력 파일 이름
        '--onefile',                      # 단일 실행 파일로 빌드
        '--clean',                        # 임시 파일 정리
        f'--distpath=dist/{platform.system().lower()}',  # OS별 출력 디렉토리
        '--add-data=wordiff/static:wordiff/static',      # static 파일 포함
        f'--version-file=version_info.txt',  # 버전 정보 파일
    ]

    # 아이콘 추가
    icon_path = get_icon_path()
    if icon_path and Path(icon_path).exists():
        args.append(f'--icon={icon_path}')

    # Windows 특정 옵션
    if platform.system() == 'Windows':
        args.extend([
            '--windowed',  # GUI 모드
        ])
    
    # macOS 특정 옵션
    elif platform.system() == 'Darwin':
        args.extend([
            '--windowed',  # GUI 모드
        ])

    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    # Windows 버전 정보 파일 생성
    if platform.system() == 'Windows':
        version_info = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION.replace('.', ', ')}, 0),
    prodvers=({VERSION.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u''),
         StringStruct(u'FileDescription', u'Word 문서 비교 도구'),
         StringStruct(u'FileVersion', u'{VERSION}'),
         StringStruct(u'InternalName', u'wordiff'),
         StringStruct(u'LegalCopyright', u''),
         StringStruct(u'OriginalFilename', u'wordiff.exe'),
         StringStruct(u'ProductName', u'WordDiff'),
         StringStruct(u'ProductVersion', u'{VERSION}')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        with open('version_info.txt', 'w', encoding='utf-8') as f:
            f.write(version_info)

    build() 