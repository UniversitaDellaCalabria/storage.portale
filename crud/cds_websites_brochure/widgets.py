from ckeditor.widgets import CKEditorWidget

class CKEditorWidgetWordCount(CKEditorWidget):
    
    def __init__(self, min_chars=-1, max_chars=-1, enforce=False, *args, **kwargs):
        self.min_chars = min_chars
        self.max_chars = max_chars
        self.enforce = enforce
        super().__init__(
            extra_plugins=['wordcount','notification',],
            *args,
            **kwargs
        ) 
        
    def _set_config(self):
        super()._set_config()
        self.config["wordcount"] = {
            'showRemaining': False,
            'showParagraphs': False,
            'showWordCount': False,
            'showCharCount': True,
            'countSpacesAsChars': True,
            'warnOnLimitOnly': False,
            'hardLimit': self.enforce,
            'maxCharCount': self.max_chars,
            #custom
            'custom': True,
            'minCharCount': self.min_chars,    
        }