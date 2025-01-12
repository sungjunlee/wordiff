import os
import sys
import traceback
from pathlib import Path
import webview
from wordiff.version import VERSION
from wordiff.core import compare_files, extract_text

# Android 플랫폼 확인
IS_ANDROID = hasattr(sys, 'getandroidapilevel')

if IS_ANDROID:
    from .android_webview import AndroidWebView
else:
    import webview

def create_api(window):
    def compare_files_api(file1_path, file2_path, ignore_space=False):
        try:
            return compare_files(file1_path, file2_path, ignore_space)
        except Exception as e:
            return False, str(e), str(e)

    def select_file():
        if IS_ANDROID:
            # Android 파일 선택 다이얼로그 호출
            intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.setType("application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            activity.startActivityForResult(intent, 1)
            # 결과는 JavaScript에서 처리
        else:
            result = window.create_file_dialog(
                webview.OPEN_DIALOG,
                file_types=('Word 문서 (*.docx)',),
                allow_multiple=False
            )
            return result[0] if result else None

    def extract_text_to_file(file_path):
        try:
            return extract_text(file_path)
        except Exception as e:
            return str(e)

    return {
        'compare_files': compare_files_api,
        'select_file': select_file,
        'extract_text_to_file': extract_text_to_file,
        'get_version': lambda: VERSION
    }

def run_gui():
    try:
        show_diff()
    except Exception as e:
        # 에러 로그를 파일로 저장
        with open('error.log', 'w') as f:
            traceback.print_exc(file=f)
        raise

def get_resource_path(relative_path):
    """PyInstaller용 리소스 경로 가져오기"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller로 실행 중
        base_path = sys._MEIPASS
    else:
        # 일반 Python으로 실행 중
        base_path = os.path.dirname(os.path.dirname(__file__))
    
    return os.path.join(base_path, relative_path)

def show_diff(file1_path=None, file2_path=None, ignore_space=False):
    # HTML 템플릿 로드
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller로 실행 중
        static_dir = Path(sys._MEIPASS) / 'static'
    else:
        # 일반 Python으로 실행 중
        static_dir = Path(__file__).parent / 'static'
    try:
        with open(static_dir / 'index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"Successfully loaded HTML from: {static_dir}")
        print(f"CSS should be at: {static_dir / 'css'}")
        if not (static_dir / 'css' / 'style.css').exists():
            print("Warning: CSS file not found!")
    except Exception as e:
        print(f"Error loading HTML: {e}")
        print(f"Current path: {os.getcwd()}")
        print(f"Static dir: {static_dir}")
        raise

    if IS_ANDROID:
        view = AndroidWebView()
        view.load_html(html_content)
    else:
        window = webview.create_window(
            'WordDiff',
            html=html_content,
            width=1000,
            height=800
        )
        
        # API 노출
        api = create_api(window)
        for name, func in api.items():
            window.expose(func)
        
        webview.start(debug=False)

if __name__ == '__main__':
    run_gui() 