from pathlib import Path
import docx

def extract_text(doc_path):
    """문서에서 텍스트 추출"""
    doc = docx.Document(doc_path)
    return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

def compare_files(file1_path, file2_path, ignore_space=False):
    """두 파일 비교"""
    text1 = extract_text(file1_path)
    text2 = extract_text(file2_path)
    
    if ignore_space:
        text1 = ''.join(text1.split())
        text2 = ''.join(text2.split())
    
    return text1 == text2, text1, text2 