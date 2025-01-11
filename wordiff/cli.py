import argparse
import colorama
from pathlib import Path
from .diff_logic import compare_docs

def main():
    parser = argparse.ArgumentParser(
        description='Word 문서(.docx) 간의 차이점을 비교합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s old.docx new.docx
  %(prog)s old.docx new.docx -c 5
  %(prog)s old.docx new.docx --ignore-space
        """
    )
    
    parser.add_argument('old_file', help='이전 버전 문서')
    parser.add_argument('new_file', help='새 버전 문서')
    parser.add_argument('-c', '--context', type=int, default=3,
                        help='차이점 주변에 표시할 문맥의 줄 수 (기본값: 3)')
    parser.add_argument('--ignore-space', action='store_true',
                        help='연속된 공백 차이를 무시합니다')
    parser.add_argument('--no-color', action='store_true',
                        help='색상 없이 출력합니다')
    parser.add_argument('-o', '--output', type=str,
                        help='결과를 파일로 저장합니다')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='차이가 없을 때 메시지를 출력하지 않습니다')

    args = parser.parse_args()

    if not args.no_color:
        colorama.init()

    try:
        diff_output = compare_docs(
            args.old_file, 
            args.new_file,
            args.context,
            args.ignore_space,
            args.no_color
        )

        if diff_output.strip():
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(diff_output)
            else:
                print(f"\n{Path(args.old_file).name}와 {Path(args.new_file).name}의 차이점:\n")
                print(diff_output)
        elif not args.quiet:
            print("차이점이 없습니다.")

    except Exception as e:
        parser.error(str(e))

if __name__ == "__main__":
    main() 