from PyQt6.QtWebEngineWidgets import QWebEngineView

class PDFPreviewer(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = self.settings()
        settings.setAttribute(self.settings().WebAttribute.PluginsEnabled, True)