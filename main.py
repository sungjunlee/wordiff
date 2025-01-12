# Android 진입점
from kivy.app import App
from kivy.utils import platform
from wordiff.gui import show_diff

class WordDiffApp(App):
    def build(self):
        # Android 권한 요청
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        return show_diff()

if __name__ == '__main__':
    WordDiffApp().run() 