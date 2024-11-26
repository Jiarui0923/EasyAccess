import markdown
import inspect
from .document import Document

class Code(Document):
    
    def __init__(self, obj, lang=''):
        if inspect.isfunction(obj):
            self._lang = 'python'
            self._obj = inspect.getsource(obj)
        elif isinstance(obj, str):
            self._lang = lang
            self._obj = obj
        else:
            raise TypeError
    
    @property     
    def markdown(self): return f'```{self._lang}\n {self._obj}\n```\n'
    @property
    def html(self): return markdown.markdown(self.markdown, extensions=['fenced_code'])