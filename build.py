import os
import sys
import shutil
from pathlib import Path
import PyInstaller.__main__

def build():
    # 현재 디렉토리를 PYTHONPATH에 추가
    sys.path.insert(0, os.path.abspath("."))

    # 운영체제별 설정
    if sys.platform.startswith('win'):
        platform = 'windows'
        ext = '.exe'
    else:
        platform = 'linux'
        ext = ''

    # 빌드 디렉토리 설정
    dist_dir = Path('dist') / platform
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True)

    # PyInstaller 옵션
    # GUI 버전 빌드
    options = [
        'wordiff/gui.py',  # GUI 진입점으로 변경
        '--name=wordiff' + ext,
        '--onefile',
        '--windowed',
        '--debug=all',  # 디버그 정보 추가
        f'--distpath={dist_dir}',
        f'--add-data=wordiff/static{os.pathsep}static',  # static 폴더만 복사
        '--icon=assets/icon.ico',
        '--clean',
    ]

    # 빌드 실행
    PyInstaller.__main__.run(options)

    # CLI 버전 빌드
    cli_options = [
        'wordiff/cli.py',
        f'--name=wordiff-cli{ext}',
        '--onefile',
        f'--distpath={dist_dir}',
        '--icon=assets/icon.ico',
        '--clean',
    ]

    # CLI 버전 빌드 실행
    PyInstaller.__main__.run(cli_options)

if __name__ == '__main__':
    build() 