from docx import Document
from pathlib import Path
import difflib
import colorama
from colorama import Fore, Style
import re

def format_diff_line(line, no_color=False):
    """한 줄의 diff를 형식화합니다."""
    if no_color:
        return line
    if line.startswith('+'):
        return f"{Fore.GREEN}{line}{Style.RESET_ALL}"
    elif line.startswith('-'):
        return f"{Fore.RED}{line}{Style.RESET_ALL}"
    elif line.startswith('@@'):
        return f"{Fore.CYAN}{line}{Style.RESET_ALL}"
    else:
        return line

def extract_text_from_docx(file_path):
    """docx 파일에서 텍스트를 추출합니다."""
    lines = []
    for paragraph in Document(file_path).paragraphs:
        # 모든 종류의 공백 문자를 일반 공백으로 변환하고 연속된 공백을 하나로
        text = re.sub(r'\s+', ' ', paragraph.text).strip()
        if text:  # 실제 내용이 있는 줄만 포함
            lines.append(text)
    return lines

def compare_docs(old_file, new_file, context_lines=3, ignore_space=False, no_color=False):
    """문서를 비교하고 차이점을 반환합니다."""
    # 파일 확장자 검사
    if not str(old_file).endswith('.docx') or not str(new_file).endswith('.docx'):
        raise ValueError("입력 파일은 .docx 형식이어야 합니다")

    # 파일 존재 여부 검사
    if not Path(old_file).exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {old_file}")
    if not Path(new_file).exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {new_file}")

    # docx 파일에서 텍스트 추출
    old_text = extract_text_from_docx(old_file)
    new_text = extract_text_from_docx(new_file)

    # unified_diff 형식으로 차이점 계산
    diff = list(difflib.unified_diff(
        old_text,
        new_text,
        fromfile=Path(old_file).name,
        tofile=Path(new_file).name,
        lineterm='',
        n=context_lines
    ))

    # 빈 줄이 연속으로 나오는 것을 방지
    filtered_diff = []
    prev_empty = False
    for line in diff:
        is_empty = not line.strip() or line.strip() in ['---', '+++']
        if not (is_empty and prev_empty):
            filtered_diff.append(line)
        prev_empty = is_empty

    return '\n'.join(format_diff_line(line, no_color) for line in filtered_diff) 