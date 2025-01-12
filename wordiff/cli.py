from .gui import print_cli_diff

def run():
    """CLI 모드 실행"""
    import sys
    return print_cli_diff(sys.argv[1], sys.argv[2]) 