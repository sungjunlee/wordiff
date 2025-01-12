# WordDiff

📄 Word 문서 비교 도구 | GUI와 CLI를 모두 지원하는 크로스 플랫폼 .docx 비교 도구

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 설치 방법

### 1. 실행 파일로 설치 (권장)

#### Windows
1. [Releases](https://github.com/sungjunlee/wordiff/releases) 페이지에서 최신 버전의 `wordiff-windows.exe` 다운로드
2. 다운로드한 파일을 실행하여 사용

#### Linux
1. [Releases](https://github.com/sungjunlee/wordiff/releases) 페이지에서 최신 버전의 `wordiff-linux` 다운로드
2. 터미널에서 실행 권한 부여:
   ```bash
   chmod +x wordiff-linux
   ```
3. 실행:
   ```bash
   ./wordiff-linux
   ```

#### macOS
macOS용 실행 파일은 개발자 인증 작업 후 추후 제공 예정입니다.
현재는 아래의 '소스코드로 설치' 방법을 이용해주세요.

### 2. 소스코드로 설치

1. Python 3.9 이상 설치
2. Poetry 설치:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. 저장소 클론:
   ```bash
   git clone https://github.com/sungjunlee/wordiff.git
   cd wordiff
   ```
4. 의존성 설치:
   ```bash
   poetry install
   ```
5. 실행:
   ```bash
   poetry run wordiff
   ```

## 사용 방법

### GUI 모드
```bash
wordiff                          # 기본 실행
wordiff file1.docx file2.docx   # 파일 자동 로드
wordiff -m file1.docx file2.docx # 수동 비교 모드
```

### CLI 모드
```bash
wordiff -c file1.docx file2.docx      # 기본 비교
wordiff -c -i file1.docx file2.docx   # 공백 무시
wordiff -c -q file1.docx file2.docx   # 조용한 모드
wordiff -c --no-color file1.docx file2.docx  # 색상 없이 출력
```

## 주요 기능
- 📊 GUI 모드: 직관적인 그래픽 인터페이스
- 💻 CLI 모드: 커맨드 라인에서 빠른 비교
- 📝 텍스트 추출: 각 문서의 텍스트를 별도 파일로 저장
- 🔍 공백 무시 옵션: 불필요한 차이 제거
- 🌈 색상 강조: 차이점을 색상으로 구분
- 🖥️ 크로스 플랫폼: Windows, macOS, Linux 지원

## 라이선스
MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.