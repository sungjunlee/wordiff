from PIL import Image
import os
from pathlib import Path

def convert_icons():
    """webp 아이콘을 각 플랫폼에 맞는 형식으로 변환합니다."""
    assets_dir = Path('assets')
    source_icon = assets_dir / 'icon.webp'
    
    if not source_icon.exists():
        print("Error: assets/icon.webp not found")
        return
    
    # 디렉토리 생성
    assets_dir.mkdir(exist_ok=True)
    
    # webp 이미지 로드
    img = Image.open(source_icon)
    
    # 256x256 크기로 리사이즈
    img = img.resize((256, 256), Image.Resampling.LANCZOS)
    
    # Windows (ICO)
    img.save(assets_dir / 'icon.ico', format='ICO')
    
    # Linux (PNG)
    img.save(assets_dir / 'icon.png', format='PNG')
    
    # macOS (PNG -> ICNS는 별도 도구 필요)
    img.save(assets_dir / 'icon_mac.png', format='PNG')
    
    print("Icons converted successfully!")
    print("Note: For macOS, you'll need to convert icon_mac.png to icon.icns manually")

if __name__ == "__main__":
    convert_icons() 