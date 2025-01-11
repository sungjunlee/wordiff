# WordDiff

📄 Word 문서 비교 도구 | GUI와 CLI를 모두 지원하는 크로스 플랫폼 .docx 비교 도구

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 소개

WordDiff는 Word 문서(.docx) 간의 차이점을 쉽게 비교할 수 있는 도구입니다. GUI 모드와 CLI 모드를 모두 지원하며, 직관적인 인터페이스를 제공합니다.

### 주요 기능

- 📊 GUI 모드: 직관적인 그래픽 인터페이스
- 💻 CLI 모드: 커맨드 라인에서 빠른 비교
- 📝 텍스트 추출: 각 문서의 텍스트를 별도 파일로 저장
- 🔍 공백 무시 옵션: 불필요한 차이 제거
- 🌈 색상 강조: 차이점을 색상으로 구분
- 🖥️ 크로스 플랫폼: Windows, macOS, Linux 지원

## 설치 방법

### 실행 파일로 설치 (권장)
[Releases](https://github.com/sungjunlee/wordiff/releases) 페이지에서 운영체제에 맞는 실행 파일을 다운로드하여 사용할 수 있습니다.

### 소스코드로 설치
```bash
# 저장소 클론
git clone https://github.com/sungjunlee/wordiff.git
cd wordiff

# Poetry로 의존성 설치
poetry install

# 실행
poetry run wordiff
```

## 사용 방법

### GUI 모드
```bash
# 기본 실행
wordiff

# 파일 자동 로드
wordiff old.docx new.docx

# 수동 비교 모드
wordiff -m old.docx new.docx
```

### CLI 모드
```bash
# 기본 비교
wordiff -c old.docx new.docx

# 공백 무시
wordiff -c -i old.docx new.docx

# 조용한 모드 (차이가 없을 때 메시지 출력 안 함)
wordiff -c -q old.docx new.docx

# 색상 없이 출력
wordiff -c --no-color old.docx new.docx
```

### 도움말
```bash
wordiff --help
```

## 개발

### 필요 사항
- Python 3.9+
- Poetry

### 개발 환경 설정
```bash
# 의존성 설치
poetry install

# 아이콘 변환
poetry run python scripts/convert_icon.py

# 실행 파일 빌드
poetry run python build.py
```

## 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.