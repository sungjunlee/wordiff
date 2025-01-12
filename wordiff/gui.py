import webview
from pathlib import Path
import json
import argparse
import colorama
from colorama import Fore, Style
import sys
from .diff_logic import compare_docs
import os
from .version import VERSION

def print_cli_diff(file1, file2, ignore_space=False, no_color=False, quiet=False):
    """CLI 모드에서 차이점을 출력합니다."""
    try:
        # 파일 확장자 검사
        if not file1.endswith('.docx') or not file2.endswith('.docx'):
            raise ValueError("입력 파일은 .docx 형식이어야 합니다")

        # 파일 존재 여부 검사
        if not Path(file1).exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file1}")
        if not Path(file2).exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file2}")

        if not no_color:
            colorama.init()

        diff_output = compare_docs(
            file1,
            file2,
            ignore_space=ignore_space,
            no_color=no_color
        )

        if diff_output.strip():
            print(f"\n{Path(file1).name}와 {Path(file2).name}의 차이점:\n")
            print(diff_output)
        elif not quiet:
            print("차이점이 없습니다.")

    except Exception as e:
        print(f"오류: {str(e)}", file=sys.stderr)
        return 1
    return 0

def create_api(window, args=None):
    def compare_files(file1_path, file2_path, ignore_space=False):
        try:
            diff_result = compare_docs(
                file1_path,
                file2_path,
                ignore_space=ignore_space,
                no_color=True
            )
            return {
                'success': True,
                'diff': diff_result,
                'file1_name': Path(file1_path).name,
                'file2_name': Path(file2_path).name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def select_file():
        result = window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=('Word 문서 (*.docx)',),
            allow_multiple=False
        )
        return result[0] if result else None

    def extract_text_to_file(file_path):
        """DOCX 파일의 텍스트를 추출하여 txt 파일로 저장합니다."""
        try:
            from .diff_logic import extract_text_from_docx
            
            # 텍스트 추출
            text_content = '\n'.join(extract_text_from_docx(file_path))
            
            # 기본 파일명 설정 (원본 파일명.txt)
            default_filename = Path(file_path).stem + '.txt'
            
            # 저장 대화상자 표시
            save_path = window.create_file_dialog(
                webview.SAVE_DIALOG,
                directory='~',
                save_filename=default_filename,
                file_types=('텍스트 파일 (*.txt)',)
            )
            
            if save_path:
                # 텍스트 파일로 저장
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                
                return {
                    'success': True,
                    'path': save_path,
                    'filename': Path(save_path).name
                }
            else:
                return {
                    'success': False,
                    'error': '저장이 취소되었습니다.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def initialize_files():
        """CLI에서 전달받은 파일들을 초기화합니다."""
        if args and args.file1 and args.file2:
            return {
                'file1': str(Path(args.file1).absolute()),
                'file2': str(Path(args.file2).absolute()),
                'auto_compare': not args.manual,
                'ignore_space': args.ignore_space
            }
        return None

    return compare_files, select_file, extract_text_to_file, initialize_files

def run_gui(file1=None, file2=None, ignore_space=False):
    parser = argparse.ArgumentParser(
        description='DOCX 차이점 비교 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s                          # GUI 모드로 실행
  %(prog)s file1.docx file2.docx    # GUI 모드로 실행하고 파일 자동 로드
  %(prog)s -m file1.docx file2.docx # GUI 모드로 실행 (수동 비교)
  %(prog)s -c file1.docx file2.docx # CLI 모드로 실행 (GUI를 띄우지 않음)
  %(prog)s -c -i file1.docx file2.docx # CLI 모드로 실행 (공백 무시)
  %(prog)s -c -q file1.docx file2.docx # CLI 모드로 실행 (조용한 모드)
  %(prog)s -c --no-color file1.docx file2.docx # CLI 모드로 실행 (색상 없음)

자세한 정보: https://github.com/sungjunlee/wordiff
        """
    )
    
    parser.add_argument('file1', nargs='?', help='이전 버전 문서')
    parser.add_argument('file2', nargs='?', help='새 버전 문서')
    parser.add_argument('--manual', '-m', action='store_true', 
                       help='수동 비교 모드 (자동 비교하지 않음)')
    parser.add_argument('--ignore-space', '-i', action='store_true', 
                       help='공백 차이 무시')
    parser.add_argument('--cli', '-c', action='store_true',
                       help='CLI 모드로 실행 (GUI를 띄우지 않음)')
    parser.add_argument('--no-color', action='store_true',
                       help='CLI 모드에서 색상 출력하지 않음')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='차이가 없을 때 메시지를 출력하지 않습니다')
    parser.add_argument('--version', '-v', action='version',
                       version=f'%(prog)s {VERSION}',
                       help='버전 정보를 출력합니다')
    
    args = parser.parse_args()

    # CLI 모드 체크
    if args.cli:
        if not (args.file1 and args.file2):
            parser.error("CLI 모드에서는 두 개의 파일을 모두 지정해야 합니다")
        return print_cli_diff(
            args.file1, 
            args.file2, 
            args.ignore_space, 
            args.no_color,
            args.quiet
        )

    # GUI 모드
    # PyInstaller 번들 지원
    if getattr(sys, 'frozen', False):
        static_dir = Path(os.environ.get('WORDIFF_STATIC', 
            Path(sys._MEIPASS) / 'wordiff' / 'static'))
    else:
        static_dir = Path(__file__).parent / 'static'
    
    template_path = static_dir / 'index.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Template not found at: {template_path}")
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body>
            <h1>Test Page</h1>
            <p>If you see this, HTML loading failed.</p>
        </body>
        </html>
        """
    
    window = webview.create_window(
        'Word 문서 비교',
        html=html_content,
        width=1000,
        height=800,
    )
    
    compare_files, select_file, extract_text_to_file, initialize_files = create_api(window, args)
    window.expose(compare_files)
    window.expose(select_file)
    window.expose(extract_text_to_file)
    window.expose(initialize_files)
    
    webview.start(debug=True)

if __name__ == "__main__":
    import sys
    sys.exit(run_gui()) 