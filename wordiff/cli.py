from wordiff.core import compare_files
from wordiff.gui import show_diff
import argparse
import sys
import io

def main():
    # GUI 모드로 실행된 경우
    if len(sys.argv) == 1:
        return show_diff()
    
    # sys.stderr가 None일 경우를 대비하여 설정
    if sys.stderr is None:
        sys.stderr = io.StringIO()
    
    parser = argparse.ArgumentParser(description='Word 문서 비교 도구')
    parser.add_argument('file1', help='첫 번째 Word 문서')
    parser.add_argument('file2', help='두 번째 Word 문서')
    parser.add_argument('--ignore-space', action='store_true', help='공백 무시')
    
    args = parser.parse_args()
    
    is_same, text1, text2 = compare_files(args.file1, args.file2, args.ignore_space)
    print(f"{'동일' if is_same else '다름'}")
    
    if not is_same:
        print("\n=== 파일1 ===")
        print(text1)
        print("\n=== 파일2 ===")
        print(text2)

if __name__ == '__main__':
    main() 