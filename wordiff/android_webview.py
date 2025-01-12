from jnius import autoclass
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
from android.storage import app_storage_path
from android.permissions import request_permissions, Permission

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')

class AndroidWebView(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
        Clock.schedule_once(self._create_webview, 0)

    def _create_webview(self, *args):
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setAllowFileAccess(True)
        webview.getSettings().setAllowContentAccess(True)
        webview.setWebViewClient(WebViewClient())
        activity.setContentView(webview)
        self.webview = webview

    def load_url(self, url):
        self.webview.loadUrl(url)

    def load_html(self, html, base_url=None):
        self.webview.loadData(html, 'text/html', 'utf-8') 